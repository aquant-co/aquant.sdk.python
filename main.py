import asyncio
import time
from datetime import datetime, timedelta
from statistics import median

from aquant import Aquant
from aquant.domains.trade.entity import OpenHighLowCloseVolume
from aquant.settings import settings

""" Only for tests purpose """


async def get_broker_example():
    aquant = await Aquant.create(
        redis_url=settings.REDIS_URL,
        nats_servers=[settings.NATS_URL],
        nats_user=settings.AQUANT_NATS_USER,
        nats_password=settings.AQUANT_NATS_PASSWORD,
    )

    try:
        df = await aquant.get_broker(21)
        return df
    finally:
        aquant.shutdown()


async def get_trades_example():
    aquant = await Aquant.create(
        redis_url=settings.REDIS_URL,
        nats_servers=[settings.NATS_URL],
        nats_user=settings.AQUANT_NATS_USER,
        nats_password=settings.AQUANT_NATS_PASSWORD,
    )

    try:
        # Parameters:
        start_time = datetime.now() - timedelta(days=100)
        end_time = datetime.now()
        ticker = "VALEO723"
        # asset = "VALE"
        # ohlcv = True
        df = await aquant.get_trades(
            ticker=ticker, start_time=start_time, end_time=end_time
        )

        # open_price = aquant.calculate_ohlcv_open(df)
        # high_price = aquant.calculate_ohlcv_high(df)
        # low_price = aquant.calculate_ohlcv_low(df)
        # close_price = aquant.calculate_ohlcv_close(df)
        # volume_quantity = aquant.calculate_ohlcv_volume(df)
        # ohlcv = aquant.calculate_ohlcv(df)

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
        df = aquant.get_current_order_book(["VALE3F_Bid"], 21)
        return df
    finally:
        aquant.shutdown()


async def get_security_example():
    aquant = await Aquant.create(
        redis_url=settings.REDIS_URL,
        nats_servers=[settings.NATS_URL],
        nats_user=settings.AQUANT_NATS_USER,
        nats_password=settings.AQUANT_NATS_PASSWORD,
    )

    try:

        # data = {
        #     # "action": "get_security_by_asset_and_expired_at",
        #     # "action": "get_security_by_asset",
        #     # "action": "get_security_by_ticker",
        #     "action": "get_security_by_asset",
        #     "params": {
        #         "asset": "VALE",
        #         # "expires_at": "2025-03-21 23:59:59.000"
        #     }
        # }

        df = await aquant.get_securities(
            asset="VALE", expires_at="2025-03-21 23:59:59.000"
        )
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

        data = await get_broker_example()

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


async def benchmark_trades():
    """
    Benchmark assíncrono simples que mede o tempo de execução em milissegundos.
    Utiliza time.perf_counter() para temporização de alta precisão e imprime informações
    sobre o tempo e os dados recuperados.
    """
    execution_times = []

    for _ in range(1):

        start_time = time.perf_counter()

        data = await get_trades_example()

        # data.get_open() => {
        #     "ticker": "abc",
        #     "open": 123864
        #     }
        # data.get_closed() => {
        #     "ticker": "abc",
        #     "closed": 123864
        #     }
        # data.get_high() => {
        #     "ticker": "abc",
        #     "high": 1234
        # }
        # etc..

        # data.get_ohlcv() => {
        #     "ticker": "ABC",
        #     "open": 123,
        #     "closed": 321,
        #     "high": 193478,
        #     "low": 1234,
        #     "volume": 19247913
        # }
        # Or data = await get_ohcv(start_time=datetime, end_time=datetime, ticker=str) =>  {
        #     ticker: "ABC",
        #     open: 123,
        #     closed: 321,
        #     high: 193478,
        #     low: 1234,
        #     volume: 19247913
        # }

        execution_time = (time.perf_counter() - start_time) * 1000
        execution_times.append(execution_time)

        await asyncio.sleep(0.1)

    min_time = min(execution_times)
    median_time = median(execution_times)
    max_time = max(execution_times)

    print("[Trades]")
    print("Resultados de Temporização (milissegundos):")
    print(
        f"Recuperados {len(data.model_dump()) if isinstance(data, OpenHighLowCloseVolume) else (len(data) if isinstance(data, dict) else 0)} registros"
    )
    print(f"\033[92mMínimo: {min_time:.2f} ms\033[0m")
    print(f"\033[93mMediana: {median_time:.2f} ms\033[0m")
    print(f"\033[91mMáximo: {max_time:.2f} ms\033[0m")
    print(
        f"\033[94mExecuções individuais: {[f'{t:.2f}' for t in execution_times]}\033[0m"
    )
    print("____")
    return min_time


async def benchmark_broker():
    """
    Benchmark assíncrono simples que mede o tempo de execução em milissegundos.
    Utiliza time.perf_counter() para temporização de alta precisão e imprime informações
    sobre o tempo e os dados recuperados.
    """
    execution_times = []

    for _ in range(5):

        start_time = time.perf_counter()

        data = await get_broker_example()

        execution_time = (time.perf_counter() - start_time) * 1000
        execution_times.append(execution_time)

        await asyncio.sleep(0.1)

    min_time = min(execution_times)
    median_time = median(execution_times)
    max_time = max(execution_times)

    print("[Broker]")
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


async def benchmark_securities():
    """
    Benchmark assíncrono simples que mede o tempo de execução em milissegundos.
    Utiliza time.perf_counter() para temporização de alta precisão e imprime informações
    sobre o tempo e os dados recuperados.
    """

    execution_times = []

    for _ in range(5):

        start_time = time.perf_counter()

        data = await get_security_example()

        execution_time = (time.perf_counter() - start_time) * 1000
        execution_times.append(execution_time)

        await asyncio.sleep(0.1)

    min_time = min(execution_times)
    median_time = median(execution_times)
    max_time = max(execution_times)

    print("[Security]")
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
    # asyncio.run(benchmark_books())
    # asyncio.run(benchmark_broker())
    # asyncio.run(benchmark_securities())
    asyncio.run(benchmark_trades())
