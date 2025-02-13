ACTIONS = {
    "ticker": "get_security_by_ticker",
    "asset": "get_security_by_asset",
    "asset_expires": "get_security_by_asset_and_expires_at",
}


def security_payload_builder(
    ticker: str | None = None, asset: str | None = None, expires_at: str | None = None
) -> dict:
    """
    Constructs the payload for the securities request based on the parameters provided.

    Args:
        ticker (Optional[str]): Ticker code.
        asset (Optional[str]): Asset code.
        expires_at (Optional[str]): Expiration date in 'YYYY-MM-DD HH:MM:SS.mmm' format.

    Returns:
        dict[str, Union[Any]: Payload configured for the get_securities method call.

    Raises:
        ValueError: If neither 'ticker' nor 'asset' are provided.
    """
    if ticker:
        return {"action": ACTIONS["ticker"], "params": {"ticker": ticker}}

    if asset:
        return {
            "action": ACTIONS["asset_expires"] if expires_at else ACTIONS["asset"],
            "params": {
                "asset": asset,
                **({"expires_at": expires_at} if expires_at else {}),
            },
        }

    raise ValueError("Informe pelo menos 'ticker' ou 'asset'.")
