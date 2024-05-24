import requests


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

    def get_loop_logs(self, period: str, index_name: str):
        """
        Получение логов по индексу.
        :param period: Период поиска (например, "2m", "1h").
        :param index_name: Имя индекса.
        """
        resp = self._session.get(
            f"{self._url}/{index_name}/_search",
            json=self.get_search_params(period),
            timeout=5,
        )
        if resp.status_code != 200:
            return {}
        return resp.json()

    @staticmethod
    def get_search_params(period: str):
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
                            "bool": {
                                "should": [
                                    {"match": {"message": "loop detected"}},
                                    {"match": {"message": "detect loop"}},
                                    {"match": {"message": "loop guard"}},
                                ]
                            }
                        },
                    ]
                }
            },
            "size": 10000,
            "_source": ["@timestamp", "message", "host"],
        }
