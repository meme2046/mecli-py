import requests
import yaml

from utils.logger import get_logger

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

    # 2. 获取以上yaml的proxies
    proxies = remote_config.get("proxies", [])

    # 3. 读取"./template.yaml",template["proxy-providers"].append({type: inline,payload=<以上的proxies>})
    with open("./template.yaml", "r", encoding="utf-8") as f:
        template = yaml.safe_load(f)

    # 添加proxies到proxy-providers
    if "proxy-providers" not in template:
        template["proxy-providers"] = []

    template["proxy-providers"].append({"type": "inline", "payload": proxies})

    # 4. 将修改后的template写入"./gen.yaml"
    with open("./mecli/gen.yaml", "w", encoding="utf-8") as f:
        yaml.dump(template, f, allow_unicode=True, default_flow_style=False)
