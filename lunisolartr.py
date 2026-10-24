"""脚本启动入口，同时保留原有的 Python 转换接口。"""

from lunisolar_cal import (
    MAX_INPUT_YEAR,
    MIN_INPUT_YEAR,
    LunisolarDate,
    SolarDate,
    lunisolar_to_solar,
    solar_to_lunisolar,
    validate_lunisolar_date,
    validate_solar_date,
)
from lunisolar_cal.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
