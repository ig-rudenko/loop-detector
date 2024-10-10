import json
from pathlib import Path

import requests

from app.settings import settings


class ElasticAPI:

    def __init__(self, url: str, token: str):
        self._url = url
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"ApiKey {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        self._match_patterns = self._load_match_patterns()

    @staticmethod
    def _load_match_patterns():
        if not Path(settings.records_patterns_file_path).exists():
            raise FileNotFoundError(f"Файл с выражениями поиска не найден: ({settings.records_patterns_file_path})")
        with open(settings.records_patterns_file_path, "r") as file:
            return json.load(file)

    def get_loop_logs(self, period: str, index_name: str):
        """
        Получение логов по индексу.
        :param period: Период поиска (например, "2m", "1h").
        :param index_name: Имя индекса.
        """
        resp = self._session.get(
            f"{self._url}/{index_name}/_search",
            json=self.get_search_params(period),
            timeout=30,
        )
        if resp.status_code != 200:
            return {}
        return resp.json()

    def get_search_params(self, period: str):
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": f"now-{period}",
                                    "lte": "now",
                                }
                            }
                        },
                        {
                            "bool": self._match_patterns
                        },
                    ]
                }
            },
            "size": 10000,
            "_source": ["@timestamp", "message", "host"],
        }
