from enum import Enum


class SecurityActions(Enum):
    """
    Security Actions Enum
    description:
        - This enum is for map all processes that are available
    """

    TICKER = "get_security_by_ticker"
    ASSET = "get_security_by_asset"
    ASSET_AND_EXPIRES_AT = "get_security_by_asset_and_expires_at"
