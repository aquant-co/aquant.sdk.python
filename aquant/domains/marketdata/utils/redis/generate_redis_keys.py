def generate_redis_keys(tickers):
    """
    Generate Redis keys based on the provided tickers.

    Args:
        tickers (list[str]): List of tickers, where each ticker may optionally
                            include a '.offer' or '.bid' suffix to specify
                            the desired data type.

    Returns:
        list[str]: List of formatted keys for querying in Redis.
    """

    keys = [
        f"aquant.stock.{base_ticker}.book.{side}"
        for ticker in tickers
        for base_ticker, sep, side in [ticker.partition(".")]
        if side in {"offer", "bid"} or not sep
        for side in (["offer", "bid"] if not sep else [side])
    ]
    return keys
