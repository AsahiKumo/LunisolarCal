import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from lunisolar_cal import MAX_INPUT_YEAR
from lunisolar_cal.cli import main


ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    def invoke(self, arguments, inputs=()):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("builtins.input", side_effect=inputs):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                status = main(arguments)
        return status, stdout.getvalue(), stderr.getvalue()

    def test_solar_short_forms(self):
        for mode in ("s", "-s"):
            with self.subTest(mode=mode):
                status, stdout, stderr = self.invoke([mode, "2024", "2", "10"])
                self.assertEqual(status, 0)
                self.assertIn("农历日期为：2024年1月1日", stdout)
                self.assertEqual(stderr, "")

    def test_lunisolar_short_forms_and_leap_flags(self):
        for mode in ("ls", "-ls"):
            for flag in ("-l", "--leap"):
                with self.subTest(mode=mode, flag=flag):
                    status, stdout, stderr = self.invoke([mode, "2023", "2", "1", flag])
                    self.assertEqual(status, 0)
                    self.assertIn("公历日期为：2023年3月22日", stdout)
                    self.assertEqual(stderr, "")

    def test_ordinary_month_is_the_default(self):
        status, stdout, stderr = self.invoke(["ls", "2023", "2", "1"])
        self.assertEqual(status, 0)
        self.assertIn("公历日期为：2023年2月20日", stdout)
        self.assertEqual(stderr, "")

    def test_invalid_dates_use_stderr_and_nonzero_status(self):
        for arguments, reason in [
            (["s", "1582", "10", "10"], "改历缺口"),
            (["s", "1900", "2", "29"], "公历日期不存在"),
            (["s", str(MAX_INPUT_YEAR + 1), "1", "1"], "年份"),
            (["ls", "2024", "1", "30"], "只有29天"),
            (["ls", "2024", "2", "1", "-l"], "不存在闰2月"),
        ]:
            with self.subTest(arguments=arguments):
                status, stdout, stderr = self.invoke(arguments)
                self.assertEqual(status, 2)
                self.assertEqual(stdout, "")
                self.assertIn(reason, stderr)

    def test_malformed_arguments_do_not_fall_back_to_input(self):
        for arguments in [
            ["unknown"], ["s", "2024", "2"], ["s", "abc", "2", "10"],
            ["s", "2024", "2", "10", "--leap"],
            ["ls", "2023", "2", "1", "--lea"], ["--"],
        ]:
            with self.subTest(arguments=arguments):
                with contextlib.redirect_stderr(io.StringIO()):
                    with patch("builtins.input", side_effect=AssertionError("unexpected input")):
                        with self.assertRaises(SystemExit) as raised:
                            main(arguments)
                self.assertEqual(raised.exception.code, 2)

    def test_help_does_not_start_interaction(self):
        for arguments in (["--help"], ["s", "--help"], ["-ls", "--help"]):
            with self.subTest(arguments=arguments):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    with self.assertRaises(SystemExit) as raised:
                        main(arguments)
                self.assertEqual(raised.exception.code, 0)
                self.assertIn("usage:", output.getvalue())

    def test_interactive_input_retry_and_leap_month_display(self):
        inputs = ["bad", " 公历 ", "abc", "2023", "13", "3", "0", "22"]
        status, stdout, stderr = self.invoke([], inputs)
        self.assertEqual(status, 0)
        self.assertIn("输入格式不正确", stdout)
        self.assertIn("农历日期为：2023年闰2月1日", stdout)
        self.assertEqual(stderr, "")

    def test_interactive_lunar_retry_and_solar_display(self):
        inputs = [" 农历 ", "2023", "2", "1", "maybe", " 是 "]
        status, stdout, stderr = self.invoke([], inputs)
        self.assertEqual(status, 0)
        self.assertIn("输入的闰月信息不正确", stdout)
        self.assertIn("公历日期为：2023年3月22日", stdout)
        self.assertEqual(stderr, "")

    def test_interactive_invalid_date_has_nonzero_status(self):
        status, stdout, stderr = self.invoke([], ["公历", "1582", "10", "10"])
        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertIn("改历缺口", stderr)

    def test_input_end_and_keyboard_interrupt(self):
        for exception, expected_status in ((EOFError, 1), (KeyboardInterrupt, 130)):
            with self.subTest(exception=exception):
                with patch("builtins.input", side_effect=exception):
                    with contextlib.redirect_stderr(io.StringIO()) as output:
                        status = main([])
                self.assertEqual(status, expected_status)
                self.assertTrue(output.getvalue().strip())

    def test_script_and_module_entry_points(self):
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        for entry in (["lunisolartr.py"], ["-m", "lunisolar_cal"]):
            for arguments, expected_status, message in [
                (["-ls", "2023", "2", "1", "-l"], 0, "2023年3月22日"),
                (["s", "1582", "10", "10"], 2, "改历缺口"),
            ]:
                with self.subTest(entry=entry, arguments=arguments):
                    result = subprocess.run(
                        [sys.executable, "-B", *entry, *arguments], input="",
                        capture_output=True, text=True, encoding="utf-8",
                        cwd=ROOT, env=env, timeout=10,
                    )
                    self.assertEqual(result.returncode, expected_status, result.stderr)
                    self.assertIn(message, result.stdout if expected_status == 0 else result.stderr)

    def test_public_imports_are_silent_and_independent_of_qt(self):
        code = (
            "import sys; import lunisolar_cal; import lunisolartr; "
            "import lunisolar_cal.formatting; "
            "assert lunisolartr.solar_to_lunisolar is lunisolar_cal.solar_to_lunisolar; "
            "assert not any(name.startswith(('PySide6', 'PyQt6')) for name in sys.modules); "
            "assert callable(lunisolartr.main)"
        )
        # 独立验证公共核心接口不会加载命令行模块。
        core_only = subprocess.run(
            [sys.executable, "-B", "-c", "import sys; import lunisolar_cal; assert 'lunisolar_cal.cli' not in sys.modules"],
            input="", capture_output=True, text=True, cwd=ROOT, timeout=10,
        )
        self.assertEqual(core_only.returncode, 0, core_only.stderr)
        result = subprocess.run(
            [sys.executable, "-B", "-c", code], input="",
            capture_output=True, text=True, cwd=ROOT, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
