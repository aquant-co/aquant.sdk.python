import asyncio
import time
from datetime import datetime, timedelta
from statistics import median

from aquant import Aquant
from aquant.settings import settings


async def get_trades_example():
    aquant = await Aquant.create(
        redis_url=settings.REDIS_URL,
        nats_servers=[settings.NATS_URL],
        nats_user=settings.AQUANT_NATS_USER,
        nats_password=settings.AQUANT_NATS_PASSWORD,
    )

    try:
        start_time = datetime.now() - timedelta(days=30)
        end_time = datetime.now()
        df = await aquant.get_trades(start_time, end_time)
        return df
    finally:
        aquant.shutdown()


async def get_current_order_book_example():
    aquant = await Aquant.create(
        redis_url=settings.REDIS_URL,
        nats_servers=[settings.NATS_URL],
        nats_user=settings.AQUANT_NATS_USER,
        nats_password=settings.AQUANT_NATS_PASSWORD,
    )

    try:
        df = aquant.get_current_order_book(["VALE3F_Bid"])
        return df
    finally:
        aquant.shutdown()


async def benchmark_books():
    """
    Benchmark assíncrono simples que mede o tempo de execução em milissegundos.
    Utiliza time.perf_counter() para temporização de alta precisão e imprime informações
    sobre o tempo e os dados recuperados.
    """
    execution_times = []

    for _ in range(5):

        start_time = time.perf_counter()

        data = await get_current_order_book_example()

        execution_time = (time.perf_counter() - start_time) * 1000
        execution_times.append(execution_time)

        await asyncio.sleep(0.1)

    min_time = min(execution_times)
    median_time = median(execution_times)
    max_time = max(execution_times)

    print("[Books]")
    print("Resultados de Temporização (milissegundos):")
    print(f"Recuperados {len(data) if data is not None else 0} registros")
    print(f"\033[92mMínimo: {min_time:.2f} ms\033[0m")
    print(f"\033[93mMediana: {median_time:.2f} ms\033[0m")
    print(f"\033[91mMáximo: {max_time:.2f} ms\033[0m")
    print(
        f"\033[94mExecuções individuais: {[f'{t:.2f}' for t in execution_times]}\033[0m"
    )
    print("____")

    return min_time


async def benchmark_trades():
    """
    Benchmark assíncrono simples que mede o tempo de execução em milissegundos.
    Utiliza time.perf_counter() para temporização de alta precisão e imprime informações
    sobre o tempo e os dados recuperados.
    """
    execution_times = []

    for _ in range(5):

        start_time = time.perf_counter()

        data = await get_trades_example()

        execution_time = (time.perf_counter() - start_time) * 1000
        execution_times.append(execution_time)

        await asyncio.sleep(0.1)

    min_time = min(execution_times)
    median_time = median(execution_times)
    max_time = max(execution_times)

    print("[Trades]")
    print("Resultados de Temporização (milissegundos):")
    print(f"Recuperados {len(data) if data is not None else 0} registros")
    print(f"\033[92mMínimo: {min_time:.2f} ms\033[0m")
    print(f"\033[93mMediana: {median_time:.2f} ms\033[0m")
    print(f"\033[91mMáximo: {max_time:.2f} ms\033[0m")
    print(
        f"\033[94mExecuções individuais: {[f'{t:.2f}' for t in execution_times]}\033[0m"
    )
    print("____")
    return min_time


if __name__ == "__main__":
    asyncio.run(benchmark_books())
    asyncio.run(benchmark_trades())
