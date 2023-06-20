import codecs
import logging
import os

import yaml

LOGGER = logging.getLogger()

CONF = None


def setup(config_dir: str, config_yaml: str):
    global CONF
    with codecs.open(os.path.join(config_dir, config_yaml), "r", "utf-8") as f:
        CONF = yaml.load(f, Loader=yaml.SafeLoader)
    LOGGER.info("[Init] Config")
    return CONF
