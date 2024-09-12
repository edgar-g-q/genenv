import json
import logging
import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from rich.logging import RichHandler

from genenv.azure.client import (
    AzureClient,
)
from genenv.env_generator import generate_env
from genenv.utils.prompt import ask_file

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler())

load_dotenv()


def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument(
        "--template",
        "-t",
        help="Template environment file. If not provided, you will be asked for it later.",
    )
    argparser.add_argument(
        "--out",
        "-o",
        help=(
            "Output path. Defaults to .env[.groupName] in the same directory as the template file."
        ),
    )
    argparser.add_argument(
        "--group",
        "-g",
        help=(
            "Variable group. "
            "See https://dev.azure.com/{organization}/{project}/_library?itemType=VariableGroups ."
        ),
    )
    argparser.add_argument(
        "--list-groups",
        "-l",
        help="List available variable groups",
        action="store_true",
    )

    example_config_path = os.path.join(os.path.dirname(__file__), "example.genenv.json")
    with open(example_config_path, "r") as f:
        example_config = json.load(f)

    argparser.add_argument(
        "--config",
        "-c",
        help=(
            f"JSON Configuration file with azure token, secrets, and additional configuration."
            f"\nExample:\n{json.dumps(example_config, indent=2)}"
        ),
        default=os.path.join(os.path.expanduser("~"), ".genenv.json"),
    )
    argparser.add_argument(
        "--verbose",
        "-v",
        help="Verbose output",
        action="store_true",
    )
    return argparser.parse_args()


def parse_config_file(config_file):
    if not os.path.exists(config_file):
        logger.error(f"Configuration file {config_file} not found")
        exit(1)
    with open(config_file, "r") as f:
        config = json.load(f)
    if "secrets" not in config:
        logger.warning('Configuration "secrets" not found')
    if "azure_token" not in config:
        logger.warning('Configuration "azure_token" not found')
    if "azure_organization" not in config:
        logger.warning('Configuration "azure_organization" not found')
    return config


def get_template_path(template_path):
    logger.info("Getting template environment file")
    if not template_path:
        template_path = ask_file(
            title="Select template environment file",
            # filters=(("Env templates", "*.env.example"), ("All files", "*.*")),
        )
    if not os.path.exists(template_path):
        logger.error(f"Template file {template_path} not found")
        exit(1)
    return template_path


def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    config = parse_config_file(args.config)

    logger.info("Getting variable groups")
    client = AzureClient(
        pat=config.get("azure_token"),
        organization=config.get("azure_organization"),
    )
    variable_groups = client.get_variable_groups("Rompetechos")
    variable_groups_per_name = {vg["name"]: vg for vg in variable_groups}
    logger.info(f"Available variable groups: {list(variable_groups_per_name.keys())}")
    if args.list_groups:
        exit(0)

    template_path = get_template_path(args.template)

    variable_group = args.group
    if not variable_group:
        variable_group = config.get("default_variable_group")
    if not variable_group:
        logger.error("No variable group provided")
        exit(1)

    out_path = args.out
    if not out_path:
        out_path = os.path.join(
            os.path.dirname(template_path),
            f".env.{variable_group}",
        )

    if os.path.exists(out_path):  # TODO ask override
        logger.warning(f"Output file {out_path} already exists. Overriding...")

    generate_env(
        template_path,
        out_path,
        variable_groups_per_name,
        variable_group,
        config.get("secrets"),
    )


if __name__ == "__main__":
    main()
