"""农历格式化。"""

from collections.abc import Callable
from .core import CalendarError, LunisolarDate, SolarDate

MONTH_NAMES = (
    "正月", "二月", "三月", "四月", "五月", "六月",
    "七月", "八月", "九月", "十月", "冬月", "腊月",
)

DAY_NAMES = (
    "初一", "初二", "初三", "初四", "初五",
    "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五",
    "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五",
    "廿六", "廿七", "廿八", "廿九", "三十",
)


def _source_text(_context: str, text: str) -> str:
    return text

def format_lunisolar(
    value: LunisolarDate,
    chinese: bool = True,
    translate: Callable[[str, str], str] = _source_text,
) -> str:
    if chinese:
        leap_text = "闰" if value.is_leap else ""
        date_text = (
            f"{value.year}年{leap_text}"
            f"{MONTH_NAMES[value.month - 1]}{DAY_NAMES[value.day - 1]}"
        )
        return translate("DateFormatting", "农历：{date}").format(
            date=date_text
        )

    if value.is_leap:
        template = translate(
            "DateFormatting", "农历：{year}年闰{month}月{day}日"
        )
    else:
        template = translate(
            "DateFormatting", "农历：{year}年{month}月{day}日"
        )

    return template.format(
        year=value.year, month=value.month, day=value.day
    )

def format_solar(
    value: SolarDate,
    translate: Callable[[str, str], str] = _source_text,
) -> str:
    template = translate(
        "DateFormatting", "公历：{year}年{month}月{day}日"
    )
    return template.format(
        year=value.year, month=value.month, day=value.day
    )


def format_calendar_error(
    error: ValueError,
    translate: Callable[[str, str], str] = _source_text,
) -> str:
    """翻译错误模板后填入参数；外部异常的原始详情保留原文。"""
    if isinstance(error, CalendarError):
        template = translate("CalendarErrors", error.template)
        reason = template.format(**error.params)
    else:
        reason = str(error)
    return translate("CalendarErrors", "输入有误：{reason}").format(reason=reason)
