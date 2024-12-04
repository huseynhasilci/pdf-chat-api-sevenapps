import logging
import json

from typing import Any

from elasticsearch import Elasticsearch
from datetime import datetime


class ElasticsearchLogger:
    def __init__(self, es_host='localhost', es_port=9200, index='my_index'):
        """

        :param es_host:
        :param es_port:
        :param index:
        """
        self.es_host = es_host
        self.es_port = es_port
        self.index = index

        es_login_url = f'http://{es_host}:{es_port}'

        self.es = Elasticsearch([es_login_url])

        self.logger = logging.getLogger('custom_logger')
        self.logger.setLevel(logging.INFO)

        es_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        es_handler.setFormatter(formatter)

        self.logger.addHandler(es_handler)

    def send_log_into_elasticsearch(self, message: Any, level: str) -> None:
        """

        :param message:
        :param level:
        :return:
        """
        message['level'] = level
        message = json.dumps(message)
        self.es.index(index=self.index, document=message)

    def save_logs_as_json(self, message: Any, log_level: str) -> None:
        ...

    def info(self, message: Any) -> None:
        """

        :param message:
        :return:
        """
        self.logger.info(message)
        self.send_log_into_elasticsearch(message, 'INFO')

    def warning(self, message: Any) -> None:
        self.logger.warning(message)
        self.send_log_into_elasticsearch(message, 'WARNING')

    def error(self, message: Any) -> None:
        self.logger.error(message)
        self.send_log_into_elasticsearch(message, 'ERROR')

    def critical(self, message: Any) -> None:
        self.logger.critical(message)
        self.send_log_into_elasticsearch(message, 'CRITICAL')

    def success(self, message: Any) -> None:
        self.logger.info(message)
        self.send_log_into_elasticsearch(message, 'SUCCESS')


a = ElasticsearchLogger()
