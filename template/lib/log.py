import codecs
import logging
import logging.config
import os

import yaml

LOGGER = logging.getLogger()


def setup(config_dir: str, log_config_yaml: str):
    with codecs.open(os.path.join(config_dir, log_config_yaml), "r", "utf-8") as f:
        log_config = f.read()
    logging.config.dictConfig(yaml.load(log_config, Loader=yaml.FullLoader))
    LOGGER.info("[Init] Logger")
