"""供命令行和桌面界面共用的历法转换接口。"""

__version__ = "1.3.1pre1"

from .core import (
    CalendarError,
    MAX_INPUT_YEAR,
    MIN_INPUT_YEAR,
    LunisolarDate,
    SolarDate,
    lunisolar_to_solar,
    solar_to_lunisolar,
    validate_lunisolar_date,
    validate_solar_date,
)

__all__ = [
    "CalendarError", "MAX_INPUT_YEAR", "MIN_INPUT_YEAR", "LunisolarDate", "SolarDate",
    "lunisolar_to_solar", "solar_to_lunisolar",
    "validate_lunisolar_date", "validate_solar_date",
]
