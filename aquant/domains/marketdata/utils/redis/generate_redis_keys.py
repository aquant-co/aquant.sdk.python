def generate_redis_keys(tickers: list[str]) -> list[str]:
    return [
        f"aquant.security.{base}.book.{side}"
        for ticker in tickers
        for base, sep, s in [ticker.partition(".")]
        if sep == "" or s in {"offer", "bid"}
        for side in (["offer", "bid"] if sep == "" else [s])
    ]
