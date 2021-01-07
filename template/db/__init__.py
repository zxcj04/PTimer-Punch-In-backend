from aclmongo import connector


def setup(config: dict):
    connector.connect.setup(config)
