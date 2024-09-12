from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def generate_env(
    template_env: str,
    out_path: str,
    variable_groups_per_name: dict,
    group_priority: str | list[str],
    secrets: dict | None = None,
):
    logger.info("Generating environment file")
    if not secrets:
        secrets = {}
    if isinstance(group_priority, str):
        group_priority = [group_priority]
    with open(template_env, "r") as f:
        in_str = f.read()

    out_str = ""

    for line in in_str.split("\n"):
        # Parse line
        is_comment = line.startswith("#")
        matches = ["=", "{{", "}}"]
        matches_ok = all([m in line for m in matches])
        equal_index = line.find("=")
        left_index = line.find("{{") + 2
        right_index = line.find("}}") - 1
        index_ok = equal_index < left_index <= right_index

        if is_comment or not matches_ok or not index_ok:
            out_str += line + "\n"
            continue

        env_name = line[:equal_index].strip()
        variable_name = line[left_index:right_index].strip()

        variable = None
        group_name = None
        for group_name in group_priority:
            group = variable_groups_per_name.get(group_name)
            if group is None:
                logging.warning(f"Group {group_name} not found")
                continue

            variable = group["variables"].get(variable_name)
            if variable is None:
                continue
            break
        if not variable:
            logging.warning(
                f"Variable {variable_name} not found in groups {group_priority}"
            )
            out_str += line + "\n"
            continue

        value = variable["value"]
        if "isSecret" in variable and variable["isSecret"]:
            value = secrets.get(group_name, {}).get(variable_name, value)
            if not value:
                logging.warning(
                    f"Secret not found for {variable_name} in {group_name}"
                )
                out_str += line + "\n"
                continue

        # Write line with value
        out_str += f"{env_name}={value}\n"

    with open(out_path, "w") as f:
        f.write(out_str)
        logger.info(f"Environment file generated at {out_path}")
