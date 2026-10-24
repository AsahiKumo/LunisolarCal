"""命令行参数与逐项输入入口；所有日期校验与转换交给 core。"""

import argparse
import sys
from collections.abc import Sequence

from . import core


def read_choice(prompt: str, choices: tuple[str, ...], error_message: str) -> str:
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print(error_message)


def read_int(prompt: str, min_value: int, max_value: int, error_message: str) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("输入格式不正确，请输入整数。")
            continue
        if min_value <= value <= max_value:
            return value
        print(error_message)


def _display_result(result: core.SolarDate | core.LunisolarDate) -> None:
    if isinstance(result, core.LunisolarDate):
        leap_text = "闰" if result.is_leap else ""
        print(f"农历日期为：{result.year}年{leap_text}{result.month}月{result.day}日")
    else:
        print(f"公历日期为：{result.year}年{result.month}月{result.day}日")


def _interactive() -> None:
    calendar = read_choice(
        "请输入日期类型（公历/农历）：",
        ("公历", "农历"),
        "输入的日期类型不正确，请输入“公历”或“农历”。",
    )
    year = read_int(
        f"请输入年份（{core.MIN_INPUT_YEAR}~{core.MAX_INPUT_YEAR}）：",
        core.MIN_INPUT_YEAR, core.MAX_INPUT_YEAR,
        f"输入的年份超出计算范围，请输入{core.MIN_INPUT_YEAR}~{core.MAX_INPUT_YEAR}之间的整数。",
    )
    month = read_int(
        "请输入月份（1~12）：", 1, 12,
        "输入的月份不合法，请输入1~12之间的整数。",
    )
    day = read_int(
        "请输入日期（1~31）：", 1, 31,
        "输入的日期不合法，请输入1~31之间的整数。",
    )
    if calendar == "公历":
        result = core.solar_to_lunisolar(year, month, day)
    else:
        is_leap = read_choice(
            "是否闰月（是/否）：", ("是", "否"),
            "输入的闰月信息不正确，请输入“是”或“否”。",
        ) == "是"
        result = core.lunisolar_to_solar(year, month, day, is_leap)
    _display_result(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="公历、农历双向转换；无参数时逐项输入。",
        epilog="s 和 -s 表示公历输入；ls 和 -ls 表示农历输入。公历采用1582年固定改历口径。",
        allow_abbrev=False,
    )
    modes = parser.add_subparsers(dest="calendar", metavar="{s,ls}", required=True)
    for name, help_text in (("s", "公历转农历"), ("ls", "农历转公历")):
        mode = modes.add_parser(name, help=help_text, description=help_text, allow_abbrev=False)
        mode.add_argument(
            "year", type=int, metavar="年",
            help=f"输入年份（{core.MIN_INPUT_YEAR}～{core.MAX_INPUT_YEAR}）",
        )
        mode.add_argument("month", type=int, metavar="月", help="月份（1～12）")
        mode.add_argument("day", type=int, metavar="日", help="日期")
        if name == "ls":
            mode.add_argument("-l", "--leap", action="store_true", help="输入的是农历闰月")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """命令行入口，返回退出码；0成功，2输入无效，1输入结束，130用户中断。"""
    arguments = list(sys.argv[1:] if argv is None else argv)
    # 将用户提供的两种简写统一交给 argparse 的同一套子命令解析。
    if arguments:
        arguments[0] = {"-s": "s", "-ls": "ls"}.get(arguments[0], arguments[0])
    try:
        if not arguments:
            _interactive()
        else:
            args = build_parser().parse_args(arguments)
            if args.calendar == "s":
                result = core.solar_to_lunisolar(args.year, args.month, args.day)
            else:
                result = core.lunisolar_to_solar(args.year, args.month, args.day, args.leap)
            _display_result(result)
    except ValueError as exc:
        print(f"输入的日期无效：{exc}", file=sys.stderr)
        return 2
    except EOFError:
        print("\n输入已结束，未完成转换。", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n已取消输入。", file=sys.stderr)
        return 130
    return 0
