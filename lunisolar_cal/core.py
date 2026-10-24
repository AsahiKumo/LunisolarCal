"""
基于 sxtwl 库的公农历算法进行公历、农历互转。
公历在 1582-10-04 及以前使用儒略历，1582-10-15 起使用格里高利历，拒绝中间的十个日期编号；这一约定不代表各地区实际采用新历的日期。
输入年份见下全局定义，输出保留库返回的年份（跨年时可能超出输入范围）。
"""

from typing import NamedTuple

import sxtwl


MIN_INPUT_YEAR = 1
MAX_INPUT_YEAR = 9999


def source_text(_context: str, text: str) -> str:
    """标记待翻译的源文字；核心层运行时保留原文。"""
    return text


class CalendarError(ValueError):
    """保存错误模板与参数，同时兼容现有 ValueError 处理。"""

    def __init__(self, template: str, **params: object) -> None:
        self.template = template
        self.params = params
        super().__init__(template.format(**params))


class SolarDate(NamedTuple):
    """按本模块改历口径表示的公历数据；校验由 validate_solar_date 完成。"""

    year: int
    month: int
    day: int


class LunisolarDate(NamedTuple):
    """以春节为年界的农历数据；闰月保留为布尔值。"""

    year: int
    month: int
    day: int
    is_leap: bool = False


def _solar_date(value: sxtwl.Day) -> SolarDate:
    return SolarDate(value.getSolarYear(), value.getSolarMonth(), value.getSolarDay())


def _lunisolar_date(value: sxtwl.Day) -> LunisolarDate:
    return LunisolarDate(
        value.getLunarYear(True), value.getLunarMonth(),
        value.getLunarDay(), value.isLunarLeap(),
    )


def _validate_date_fields(year: int, month: int, day: int, max_day: int) -> None:
    if any(type(value) is not int for value in (year, month, day)):
        raise CalendarError(source_text("CalendarErrors", "年、月、日必须是整数。"))
    if not MIN_INPUT_YEAR <= year <= MAX_INPUT_YEAR:
        raise CalendarError(
            source_text("CalendarErrors", "输入年份必须在{min_year}～{max_year}之间。"),
            min_year=MIN_INPUT_YEAR, max_year=MAX_INPUT_YEAR,
        )
    if not 1 <= month <= 12:
        raise CalendarError(source_text("CalendarErrors", "月份必须在1～12之间。"))
    if not 1 <= day <= max_day:
        raise CalendarError(
            source_text("CalendarErrors", "日期必须在1～{max_day}之间。"),
            max_day=max_day,
        )


def _validated_solar_day(year: int, month: int, day: int) -> sxtwl.Day:
    _validate_date_fields(year, month, day, 31)
    if (1582, 10, 5) <= (year, month, day) <= (1582, 10, 14):
        raise CalendarError(source_text(
            "CalendarErrors", "1582年10月5日至14日属于改历缺口，在本程序采用的历法中不存在。",
        ))
    try:
        value = sxtwl.fromSolar(year, month, day)
        converted = _solar_date(value)
    except Exception as exc:
        raise CalendarError(
            source_text("CalendarErrors", "无法解析公历日期：{detail}"),
            detail=str(exc),
        ) from exc
    # 库会归一化无效日期；通过原样往返检查月长和对应历法的闰年规则。
    if converted != SolarDate(year, month, day):
        raise CalendarError(source_text(
            "CalendarErrors", "公历日期不存在，请检查该月的天数和闰年规则。",
        ))
    return value


def _validated_lunisolar_day(
    year: int, month: int, day: int, is_leap: bool,
) -> sxtwl.Day:
    _validate_date_fields(year, month, day, 30)
    if type(is_leap) is not bool:
        raise CalendarError(source_text(
            "CalendarErrors", "is_leap 必须是布尔值 True 或 False。",
        ))
    try:
        leap_month = sxtwl.getRunMonth(year)
        month_days = sxtwl.getLunarMonthNum(year, month, is_leap)
    except Exception as exc:
        raise CalendarError(
            source_text("CalendarErrors", "无法查询农历月份：{detail}"),
            detail=str(exc),
        ) from exc
    if is_leap and leap_month != month:
        raise CalendarError(
            source_text("CalendarErrors", "{year}年不存在闰{month}月。"),
            year=year, month=month,
        )
    if day > month_days:
        if is_leap:
            template = source_text("CalendarErrors", "{year}年闰{month}月只有{days}天。")
        else:
            template = source_text("CalendarErrors", "{year}年{month}月只有{days}天。")
        raise CalendarError(template, year=year, month=month, days=month_days)
    try:
        value = sxtwl.fromLunar(year, month, day, is_leap)
        solar = _solar_date(value)
        lunar_back = _lunisolar_date(sxtwl.fromSolar(*solar))
    except Exception as exc:
        raise CalendarError(
            source_text("CalendarErrors", "无法解析农历日期：{detail}"),
            detail=str(exc),
        ) from exc
    if lunar_back != LunisolarDate(year, month, day, is_leap):
        raise CalendarError(source_text(
            "CalendarErrors", "农历日期往返校验不一致，请核对年月日及闰月信息。",
        ))
    return value


def validate_solar_date(year: int, month: int, day: int) -> None:
    """校验本模块口径下的公历日期；无效时抛出带原因的 ValueError。"""
    _validated_solar_day(year, month, day)


def validate_lunisolar_date(
    year: int, month: int, day: int, is_leap: bool = False,
) -> None:
    """校验农历年月日及闰月标志；无效时抛出带原因的 ValueError。"""
    _validated_lunisolar_day(year, month, day, is_leap)


def solar_to_lunisolar(year: int, month: int, day: int) -> LunisolarDate:
    """输入公历年月日，校验后返回农历数据；无效时抛出 ValueError。"""
    return _lunisolar_date(_validated_solar_day(year, month, day))


def lunisolar_to_solar(
    year: int, month: int, day: int, is_leap: bool = False,
) -> SolarDate:
    """输入农历年月日及闰月标志，校验后返回公历数据。"""
    return _solar_date(_validated_lunisolar_day(year, month, day, is_leap))
