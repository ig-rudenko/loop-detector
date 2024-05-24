from threading import Thread

from loguru import logger

from app.loopd import GraphLoopBuilder
from app.services.cache import get_cache
from app.services.decorators import time_sleep_after
from app.services.ecstasy import EcstasyAPI
from app.services.elastic import ElasticAPI
from app.services.log_parser import get_records, Record
from app.services.logging import setup_logger
from app.settings import settings


@time_sleep_after(120)
@logger.catch
def main(ecstasy_api: EcstasyAPI, elastic_api: ElasticAPI):
    logs_data = elastic_api.get_loop_logs(settings.loop_period, settings.es_index)

    cache = get_cache()
    cache_key = "loop_detected_records"
    # Получаем прошлые логи из кеша.
    past_logs_records: list[Record] = cache.get(cache_key) or []
    new_logs_records = get_records(logs_data)

    all_records = past_logs_records + new_logs_records
    # Сохраняем все логи в кеш, чтобы их можно было использовать в будущем.
    cache.set(cache_key, value=all_records, timeout=5 * 60)

    builder = GraphLoopBuilder(elastic_api=elastic_api, ecstasy_api=ecstasy_api)
    builder.build_initial_devices(all_records)
    builder.create_initial_graph()

    for _ in range(3):
        builder.increase_graph_depth()
        graph_data = builder.graph.build_graph()
        logger.info("Built graph data", graph_depth=builder.graph_depth)
        cache.set(f"currentLoop:depth={builder.graph_depth}", value=graph_data, timeout=6 * 60 * 60)


if __name__ == "__main__":
    setup_logger(settings.log_level)

    while True:
        logger.info("Запуск программы")
        ecstasy = EcstasyAPI(
            url=settings.ecstasy_url, username=settings.ecstasy_username, password=settings.ecstasy_password
        )
        elastic = ElasticAPI(f"{settings.es_host}:{settings.es_port}", token=settings.es_token)
        thread = Thread(target=main, args=(ecstasy, elastic), name="loopd")

        try:
            thread.start()
            thread.join()
        except KeyboardInterrupt:
            logger.info("Завершение программы.")
            break
