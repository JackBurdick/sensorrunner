import crummycm as ccm
from aeropi.config.template import TEMPLATE as DEFAULT_TEMPLATE


def start_tasks_from_config(config_path: str, template=DEFAULT_TEMPLATE):
    config = ccm.generate(config_path, template=template)
    print(config)
