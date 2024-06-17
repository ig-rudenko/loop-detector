from threading import Thread

from loguru import logger

from app.loopd import GraphLoopBuilder
from app.services.cache import get_cache
from app.services.decorators import time_sleep_after
from app.services.ecstasy import EcstasyAPI
from app.services.elastic import ElasticAPI
from app.services.graph_writter import write_graph
from app.services.log_parser import get_records
from app.services.log_recorder import LogsRecorder
from app.services.logging import setup_logger
from app.settings import settings


@time_sleep_after(120)
@logger.catch
def main(ecstasy_api: EcstasyAPI, elastic_api: ElasticAPI):
    logs_data = elastic_api.get_loop_logs(settings.loop_period, settings.es_index)
    new_logs_records = get_records(logs_data)

    recorder = LogsRecorder(new_logs_records)
    all_records = recorder.get_all_logs_records()
    loop_name = recorder.get_loop_name()
    recorder.save()

    builder = GraphLoopBuilder(elastic_api=elastic_api, ecstasy_api=ecstasy_api)
    builder.build_initial_devices(all_records)
    builder.create_initial_graph()

    cache = get_cache()
    for i in range(3):
        builder.increase_graph_depth()
        graph_data = builder.graph.build_graph()
        logger.info("Built graph data", graph_depth=builder.graph_depth)
        cache.set(f"currentLoop:depth={builder.graph_depth}", value=graph_data, timeout=6 * 60 * 60)
        if i == 2:
            write_graph(graph_data, loop_name)


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
