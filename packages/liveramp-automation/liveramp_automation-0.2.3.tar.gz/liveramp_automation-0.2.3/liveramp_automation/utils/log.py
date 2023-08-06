# -*- coding: utf-8 -*-
import configparser
import os
import logging
from datetime import datetime
from logging import handlers
from threading import Lock


class LoggerUtils:
    """
    This object is a single pattern instance to log.
    If we haven't set the default log_path in the pytest.ini file, it would use the path = "reports/"
    If we haven't set the default log_name in the pytest.ini file, it would use the log_name = "%Y%m%d%H%M%S.log"
    :param
    :type
    :return:
    :rtype:
    :raises
    """
    _instance = None
    _lock = Lock()

    @classmethod
    def get_logger(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls._configure_logging()
        return cls._instance

    @staticmethod
    def _configure_logging():
        config = configparser.ConfigParser()
        try:
            with open("pytest.ini", 'r') as file:
                config.read_file(file)
                try:
                    log_path = config.get('log', 'log_path')
                except (configparser.NoSectionError, configparser.NoOptionError):
                    log_path = "reports/"
                try:
                    log_name = config.get('log', 'log_name')
                except (configparser.NoSectionError, configparser.NoOptionError):
                    log_name = "%Y%m%d%H%M%S.log"
        except FileNotFoundError:
            log_path = "reports/"
            log_name = "%Y%m%d%H%M%S.log"
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - [ %(filename)s: %(lineno)d ] - %(message)s')
        log_directory = os.path.join(os.getcwd(), log_path)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_name = datetime.now().strftime(log_name)
        file_name = os.path.join(log_path, log_name)

        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        file_handler = handlers.TimedRotatingFileHandler(filename=file_name, when='midnight', backupCount=30,
                                                         encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        logger.debug("======Now LOG BEGIN=======")
        return logger


Logger = LoggerUtils.get_logger()
