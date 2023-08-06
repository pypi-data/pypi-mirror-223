import os
import re
import sys
import yaml
import hashlib

from dataclasses import dataclass

from hcloud import Client
from hcloud.images.domain import Image
from hcloud.ssh_keys.domain import SSHKey

import testflows.github.runners.args as args

from .actions import Action

# add support for parsing ${ENV_VAR} in config
env_pattern = re.compile(r".*?\${(.*?)}.*?")


def env_constructor(loader, node):
    value = loader.construct_scalar(node)
    for group in env_pattern.findall(value):
        value = value.replace(f"${{{group}}}", os.environ.get(group))
    return value


yaml.add_implicit_resolver("!pathex", env_pattern)
yaml.add_constructor("!pathex", env_constructor)


class ImageNotFoundError(Exception):
    pass


path = args.path_type
count = args.count_type
image = args.image_type
location = args.location_type
server_type = args.server_type
end_of_life = args.end_of_life_type


@dataclass
class standby_runner:
    labels: list[str]
    count: count = 1
    replenish_immediately: bool = True


@dataclass
class deploy:
    server_type: server_type = server_type("cpx11")
    image: image = image("x86:system:ubuntu-22.04")
    location: location = None
    setup_script: path = None


@dataclass
class cloud:
    server_name: str = "github-runners"
    deploy: deploy = deploy()


@dataclass
class Config:
    """Program configuration class."""

    github_token: str = os.getenv("GITHUB_TOKEN")
    github_repository: str = os.getenv("GITHUB_REPOSITORY")
    hetzner_token: str = os.getenv("HETZNER_TOKEN")
    ssh_key: str = os.path.expanduser("~/.ssh/id_rsa.pub")
    ssh_keys: list[str] = None
    with_label: str = None
    recycle: bool = True
    end_of_life: count = 50
    max_runners: count = 10
    max_runners_in_workflow_run: count = None
    default_image: image = image("x86:system:ubuntu-22.04")
    default_server_type: server_type = server_type("cx11")
    default_location: location = None
    workers: count = 10
    setup_script: path = None
    startup_x64_script: path = None
    startup_arm64_script: path = None
    max_powered_off_time: count = 60
    max_unused_runner_time: count = 120
    max_runner_registration_time: count = 120
    max_server_ready_time: count = 120
    scale_up_interval: count = 15
    scale_down_interval: count = 15
    debug: bool = False
    # special
    logger_config: dict = None
    cloud: cloud = cloud()
    standby_runners: list[standby_runner] = None
    server_prices: dict[str, float] = None
    config_file: path = None

    def __post_init__(self):
        if self.standby_runners is None:
            self.standby_runners = []

        if self.ssh_keys is None:
            self.ssh_keys = []

    def update(self, args):
        """Update configuration file using command line arguments."""
        for attr in vars(self):
            if attr in [
                "config_file",
                "logger_config",
                "cloud",
                "standby_runners",
                "ssh_keys",
                "server_prices",
            ]:
                continue

            arg_value = getattr(args, attr)

            if arg_value is not None:
                setattr(self, attr, arg_value)

        if getattr(args, "cloud_server_name", None) is not None:
            self.cloud.server_name = args.cloud_server_name

        if getattr(args, "cloud_deploy_location", None) is not None:
            self.cloud.deploy.location = args.cloud_deploy_location

        if getattr(args, "cloud_deploy_server_type", None) is not None:
            self.cloud.deploy.server_type = args.cloud_deploy_server_type

        if getattr(args, "cloud_deploy_image", None) is not None:
            self.cloud.deploy.image = args.cloud_deploy_image

        if getattr(args, "cloud_deploy_setup_script", None) is not None:
            self.cloud.deploy.setup_script = args.cloud_deploy_setup_script

    def check(self, *parameters):
        """Check mandatory configuration parameters."""

        if not parameters:
            parameters = ["github_token", "github_repository", "hetzner_token"]

        for name in parameters:
            value = getattr(self, name)
            if value:
                continue
            print(
                f"argument error: --{name.lower().replace('_','-')} is not defined",
                file=sys.stderr,
            )
            sys.exit(1)


def read(path: str):
    """Load raw configuration document."""
    with open(path, "r") as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def write(file, doc: dict):
    """Write raw configuration document to file."""
    yaml.dump(doc, file)


def parse_config(path: str):
    """Load and parse yaml configuration file into config object."""
    with open(path, "r") as f:
        doc = yaml.load(f, Loader=yaml.SafeLoader)

    if doc.get("cloud"):
        doc["cloud"] = cloud(
            doc["cloud"], deploy=deploy(**doc["cloud"].get("deploy", {}))
        )

    if doc.get("standby_runners"):
        doc["standby_runners"] = [
            standby_runner(**entry) for entry in doc["standby_runners"]
        ]

    return Config(**doc)


def check_ssh_key(client: Client, ssh_key: str):
    """Check that ssh key exists if not create it."""

    with open(ssh_key, "r", encoding="utf-8") as ssh_key_file:
        public_key = ssh_key_file.read()

    key_name = hashlib.md5(public_key.encode("utf-8")).hexdigest()
    ssh_key = SSHKey(name=key_name, public_key=public_key)

    if not client.ssh_keys.get_by_name(name=ssh_key.name):
        with Action(f"Creating SSH key {ssh_key.name}", stacklevel=3):
            client.ssh_keys.create(name=ssh_key.name, public_key=ssh_key.public_key)

    return ssh_key


def check_image(client: Client, image: Image):
    """Check if image exists.
    If image type is not 'system' then use image description to find it.
    """

    if image.type in ("system", "app"):
        return client.images.get_by_name_and_architecture(
            name=image.name, architecture=image.architecture
        )
    else:
        # backup or snapshot
        try:
            return [
                i
                for i in client.images.get_all(
                    type=image.type, architecture=image.architecture
                )
                if i.description == image.description
            ][0]
        except IndexError:
            raise ImageNotFoundError(f"{image.type}:{image.description} not found")
