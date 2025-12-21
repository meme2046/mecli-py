import os

import requests
import yaml
from dotenv import load_dotenv

from utils.logger import get_logger

load_dotenv("d:/.env")
logger = get_logger(__name__)


def get_clash_yaml(url, user_agent, proxy: str | None = None):
    headers = {"User-Agent": user_agent} if user_agent else {}
    proxies = None
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy,
        }

    response = requests.get(url, headers=headers, proxies=proxies)
    response.raise_for_status()
    logger.debug(f"Subscription:${response.headers['Subscription-Userinfo']}")
    remote_config = yaml.safe_load(response.text)

    proxies = remote_config.get("proxies", [])
    if not proxies:
        logger.error("No proxies found in subscription.")
        return

    try:
        with open("./data/template.yaml", "r", encoding="utf-8") as f:
            template = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing template.yaml: {e}")
        return
    except FileNotFoundError:
        logger.error("template.yaml file not found")
        return

    if "proxy-providers" not in template:
        template["proxy-providers"] = []

    template["proxy-providers"].append({"type": "inline", "payload": proxies})

    try:
        with open("./data/gen.yaml", "w", encoding="utf-8") as f:
            yaml.dump(template, f, allow_unicode=True, default_flow_style=False)
    except Exception as e:
        logger.error(f"Error writing to gen.yaml: {e}")


if __name__ == "__main__":
    get_clash_yaml(
        os.getenv("GOUGOU_SUB_API"),
        "clash-verge/v2.4.3",
    )
