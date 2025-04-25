from enum import Enum


class TimescaleIntervalEnum(Enum):
    """Enum for timescale intervals."""

    MINUTE_1 = "1 minute"
    MINUTE_5 = "5 minutes"
    MINUTE_15 = "15 minutes"
    MINUTE_30 = "30 minutes"
    HOUR_1 = "1 hour"
    HOUR_2 = "2 hours"
    HOUR_4 = "4 hours"
    HOUR_6 = "6 hours"
    HOUR_8 = "8 hours"
    HOUR_12 = "12 hours"
    DAY_1 = "1 day"
    DAY_3 = "3 days"
    DAY_5 = "5 days"
    DAY_7 = "7 days"
    DAY_15 = "15 days"
    MONTH_1 = "1 month"
    MONTH_3 = "3 months"
    MONTH_6 = "6 months"
    YEAR_1 = "1 year"
