import contextlib
import io
import unittest
from unittest.mock import patch

from lunisolar_cal import core as cal
from lunisolar_cal.formatting import format_calendar_error


class CalendarValidationTests(unittest.TestCase):
    def test_valid_solar_dates_under_calendar_policy(self):
        for date in [
            (1, 1, 1), (100, 2, 29), (1500, 2, 29),
            (1582, 10, 4), (1582, 10, 15), (1600, 2, 29),
            (2000, 2, 29), (2024, 2, 29), (cal.MAX_INPUT_YEAR, 12, 31),
        ]:
            with self.subTest(date=date):
                self.assertIsNone(cal.validate_solar_date(*date))

    def test_invalid_solar_dates(self):
        for date in [
            (0, 1, 1), (cal.MAX_INPUT_YEAR + 1, 1, 1), (2024, 0, 1), (2024, 13, 1),
            (2024, 1, 0), (2024, 1, 32), (2024, 4, 31),
            (1501, 2, 29), (1700, 2, 29), (1900, 2, 29), (2023, 2, 29),
            (True, 1, 1), (2024.0, 1, 1), (2024, "2", 1),
        ]:
            with self.subTest(date=date), self.assertRaises(ValueError):
                cal.validate_solar_date(*date)

    def test_all_ten_reform_gap_dates_are_rejected(self):
        for day in range(5, 15):
            with self.subTest(day=day), self.assertRaisesRegex(ValueError, "改历缺口"):
                cal.solar_to_lunisolar(1582, 10, day)

    def test_reform_boundary_preserves_lunar_day_sequence(self):
        self.assertEqual(
            cal.solar_to_lunisolar(1582, 10, 4),
            cal.LunisolarDate(1582, 9, 18, False),
        )
        self.assertEqual(
            cal.solar_to_lunisolar(1582, 10, 15),
            cal.LunisolarDate(1582, 9, 19, False),
        )

    def test_lunar_month_length_and_leap_month(self):
        cal.validate_lunisolar_date(1, 1, 1)
        cal.validate_lunisolar_date(2024, 1, 29)
        cal.validate_lunisolar_date(2023, 2, 1, True)
        for date, reason in [
            ((2024, 1, 30, False), "只有29天"),
            ((2024, 2, 1, True), "不存在闰2月"),
            ((2023, 1, 1, True), "不存在闰1月"),
            ((2024, 1, 31, False), "1～30"),
            ((2024, 1, 1, "否"), "布尔值"),
            ((2024, 1, 1, 1), "布尔值"),
            ((0, 1, 1, False), "年份"),
            ((cal.MAX_INPUT_YEAR + 1, 1, 1, False), "年份"),
        ]:
            with self.subTest(date=date), self.assertRaisesRegex(ValueError, reason):
                cal.lunisolar_to_solar(*date)

    def test_conversion_results_have_named_fields_and_boolean_leap_flag(self):
        new_year = cal.solar_to_lunisolar(2024, 2, 10)
        leap_month = cal.solar_to_lunisolar(2023, 3, 22)
        self.assertEqual(new_year, cal.LunisolarDate(2024, 1, 1, False))
        self.assertEqual(leap_month, cal.LunisolarDate(2023, 2, 1, True))
        self.assertIs(new_year.is_leap, False)
        self.assertIs(leap_month.is_leap, True)
        self.assertEqual(
            cal.lunisolar_to_solar(*new_year), cal.SolarDate(2024, 2, 10),
        )
        self.assertEqual(
            cal.lunisolar_to_solar(*leap_month), cal.SolarDate(2023, 3, 22),
        )

    def test_solar_lunar_round_trip(self):
        for date in [
            (1500, 2, 29), (1582, 10, 4), (1582, 10, 15),
            (1700, 3, 1), (2000, 2, 29), (cal.MAX_INPUT_YEAR, 12, 31),
        ]:
            with self.subTest(date=date):
                self.assertEqual(
                    cal.lunisolar_to_solar(*cal.solar_to_lunisolar(*date)),
                    cal.SolarDate(*date),
                )

    def test_output_year_is_not_truncated_to_input_range(self):
        self.assertEqual(cal.solar_to_lunisolar(1, 1, 1).year, 0)
        self.assertEqual(cal.lunisolar_to_solar(cal.MAX_INPUT_YEAR, 12, 29).year, cal.MAX_INPUT_YEAR + 1)

    def test_validation_and_conversion_do_not_print(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            cal.validate_solar_date(1500, 2, 29)
            cal.solar_to_lunisolar(2024, 2, 10)
            with self.assertRaises(ValueError):
                cal.validate_lunisolar_date(2024, 1, 30)
        self.assertEqual(output.getvalue(), "")

    def test_error_translation_uses_template_before_inserting_values(self):
        with self.assertRaises(cal.CalendarError) as raised:
            cal.lunisolar_to_solar(2024, 2, 1, True)
        error = raised.exception
        self.assertIsInstance(error, ValueError)
        self.assertEqual(error.args, ("2024年不存在闰2月。",))
        self.assertEqual(error.params, {"year": 2024, "month": 2})
        translations = {
            "{year}年不存在闰{month}月。": "Year {year} has no leap month {month}.",
            "输入有误：{reason}": "Invalid input: {reason}",
        }
        result = format_calendar_error(error, lambda context, text: translations[text])
        self.assertEqual(result, "Invalid input: Year 2024 has no leap month 2.")
        self.assertEqual(format_calendar_error(error), "输入有误：2024年不存在闰2月。")

    def test_leap_month_length_error_has_a_translatable_leap_marker(self):
        with self.assertRaises(cal.CalendarError) as raised:
            cal.lunisolar_to_solar(2023, 2, 30, True)
        translations = {
            "{year}年闰{month}月只有{days}天。":
                "Year {year}, leap month {month} has only {days} days.",
            "输入有误：{reason}": "Invalid input: {reason}",
        }
        result = format_calendar_error(
            raised.exception, lambda context, text: translations[text],
        )
        self.assertEqual(result, "Invalid input: Year 2023, leap month 2 has only 29 days.")

    def test_backend_error_keeps_its_cause_and_literal_detail(self):
        failure = RuntimeError("backend {detail}")
        with patch.object(cal.sxtwl, "fromSolar", side_effect=failure):
            with self.assertRaises(cal.CalendarError) as raised:
                cal.solar_to_lunisolar(2024, 2, 10)
        self.assertIs(raised.exception.__cause__, failure)
        self.assertEqual(raised.exception.params, {"detail": "backend {detail}"})
        self.assertEqual(str(raised.exception), "无法解析公历日期：backend {detail}")


if __name__ == "__main__":
    unittest.main()
