import logging

import anyconfig
from attrdict import AttrDict
from pkg_resources import resource_filename

logger = logging.getLogger(__name__)


def normalize_config(config):
    if config.mqtt.topic_set_prefix.endswith('/'):
        logger.warning("value mqtt.topic_set should not end with a /")
        config.mqtt.topic_set = config.mqtt.topic_set.rstrip('/')

    if config.mqtt.topic_status_prefix.endswith('/'):
        logger.warning("value mqtt.topic_status should not end with a /")
        config.mqtt.topic_status = config.mqtt.topic_status.rstrip('/')
    return config


def load_config(path):
    default_configuration = anyconfig.load(resource_filename('cecmqtt.config', 'default.yaml'))
    try:
        config = anyconfig.load(path)
    except IOError:
        logger.warning("no config file found at: %s", path)
        config = {}
    config = default_configuration + AttrDict(config)
    return normalize_config(config)
