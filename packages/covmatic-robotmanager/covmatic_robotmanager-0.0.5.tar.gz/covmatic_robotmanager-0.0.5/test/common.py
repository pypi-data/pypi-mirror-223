import sys
import unittest
import logging
from src.covmatic_robotmanager.config import Config


def setup_log():
    logger = logging.getLogger()
    logger.level = logging.DEBUG


class BaseTestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_fake_config_args()

    @staticmethod
    def set_fake_config_args():
        Config().eva_ip = ""
        Config().eva_token = ""


