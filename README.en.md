# LunisolarCal

[简体中文](README.md) | **English**

A solar-lunisolar calendar converter based on `sxtwl`, with a Qt desktop interface, a command-line interface, and a Python API. It supports leap-month input and date validation.

OpenAI Codex was used during development to assist with coding, debugging, documentation, and UI icons.

> **First time here?** Start with [Quick start](#quick-start). Extract and run the Windows desktop bundle; no Python or Pixi installation is required. Development and packaging instructions are in [Developers](#developers).

- The desktop interface supports Simplified Chinese, English, and system language matching.
- Features include today's date, Chinese lunisolar notation, copying results, and keyboard shortcuts.
- The About dialog provides version information, the project homepage, and a local license viewer.

> Probably no one is going to use this thing of mine anyway...

## Contents

**Users:** [Quick start](#quick-start) · [Desktop interface](#using-the-desktop-interface) · [Command line](#command-line) · [Troubleshooting](#troubleshooting) · [Calendar conventions](#supported-years-and-calendar-conventions)

**Developers:** [Dependencies](#environment-and-dependencies) · [Project structure](#project-structure) · [UI and icons](#editing-the-interface-and-icons) · [Translations](#maintaining-interface-translations) · [Python API](#python-api) · [Tests](#tests) · [Packaging](#windows-packaging)

**Other:** [Licenses](#license-and-third-party-components) · [References](#references) · [Report an issue](https://github.com/AsahiKumo/LunisolarCal/issues)

---

## Users

### Quick start

#### Windows desktop app

1. **Download.** Get `LunisolarCal-<version>-win64.zip` from [Releases](https://github.com/AsahiKumo/LunisolarCal/releases/latest).
2. **Extract.** Extract all files from the ZIP into a folder.
3. **Run.** Double-click `LunisolarCal.exe` inside that folder to open the converter.

Python and Pixi are not required. Keep the adjacent `_internal` and `licenses` directories and documentation files; move or share the entire folder together.

#### Run from source

1. Install [Pixi](https://pixi.prefix.dev/latest/installation/).
2. Open PowerShell in the project root (the directory containing `pixi.toml`) and install the environment:

   ```powershell
   pixi install --locked
   ```

3. Start the desktop interface:

   ```powershell
   pixi run python -m lunisolar_cal.gui
   ```

Run all commands below from the project root. To use the desktop ZIP, follow the Windows steps above.

### Using the desktop interface

1. Select the input calendar: Solar or Lunisolar.
2. Enter the year, month, and day. Select "Leap month (lunisolar)" when entering a leap month.
3. When converting a solar date to a lunisolar date, optionally enable "Chinese lunisolar notation" to display names such as `正月`, `闰二月`, and `初一`.
4. Click "Convert" to display the date in the other calendar.

The leap-month option is disabled for solar input; Chinese lunisolar notation is disabled for lunisolar input. Invalid dates produce an explanation in the result area. Changing the input or interface language resets the result to "Waiting for conversion"; convert again to calculate a new result.

Common actions:

| Action | Description |
| --- | --- |
| Today | Keep the selected input calendar, fill in today's corresponding date, and convert |
| Copy result | Copy the most recent successful result; disabled after an input change or a failed conversion |
| Language | Choose Simplified Chinese, English, or Follow system; Chinese lunisolar notation can be selected independently |
| About → Licenses | View project information, third-party component notices, and license texts; Markdown notices are rendered with formatting |

"Follow system" matches the system's preferred interface languages against Chinese and English. All Chinese language variants, including Traditional Chinese locales, currently use Simplified Chinese. If no supported language matches, the interface falls back to English.

| Shortcut | Action |
| --- | --- |
| `Enter` | Convert |
| `Alt+T` | Fill in today's date and convert |
| `Ctrl+Shift+C` | Copy a valid result |
| `Tab` / `Shift+Tab` | Move focus between controls |

You can also select and copy text directly from the result area.

### Command line

Convert a date directly:

```powershell
# Solar 2024-02-10 → lunisolar year 2024, month 1, day 1
pixi run cal s 2024 2 10

# Lunisolar year 2023, regular month 2, day 1 → solar 2023-02-20
pixi run cal ls 2023 2 1

# Lunisolar year 2023, leap month 2, day 1 → solar 2023-03-22
pixi run cal ls 2023 2 1 -l
```

`s` selects solar input, and `ls` selects lunisolar input. You can also use `-s` and `-ls`, respectively. A lunisolar month is treated as a regular month by default; use `-l` or `--leap` for a leap month.

To enter the date interactively, run without arguments:

```powershell
pixi run cal
```

View command-line help:

```powershell
pixi run cal --help
pixi run cal ls --help
```

The CLI currently uses Chinese prompts, help text, and output. The desktop language setting applies only to the GUI.

### Troubleshooting

| Symptom | What to do |
| --- | --- |
| The download does not contain `LunisolarCal.exe` | Choose `LunisolarCal-<version>-win64.zip` from Releases. GitHub's automatically generated `Source code` archives require the [source environment](#run-from-source) |
| The leap-month option is disabled | Select Lunisolar as the input calendar. This option is disabled for solar input |
| Changing the date resets the result and disables copying | Click Convert again. Copy result is available only after a successful conversion |
| The English interface still shows Chinese date names such as `闰二月` or `初一` | Uncheck `Chinese lunisolar notation`. The interface language and date notation are separate settings |
| A date or leap month is rejected | Check the month length, leap-month selection, and whether that year has the requested leap month. See [calendar conventions](#supported-years-and-calendar-conventions) for the 1582 reform gap and other rules |

If the problem persists, [open an issue](https://github.com/AsahiKumo/LunisolarCal/issues) with the application version, input calendar, date, leap-month selection, interface language, and error message so it can be reproduced.

### Supported years and calendar conventions

- **Input years range from `1` to `9999`.** Conversions across a year boundary may produce lunisolar year 0 or solar year 10000, which are outside the accepted input range.
- Solar dates **on or before 1582-10-04 use the Julian calendar**; dates **from 1582-10-15 onward use the Gregorian calendar**. Dates from 1582-10-05 through 1582-10-14 are rejected as a calendar reform gap. This is the application's fixed convention; actual adoption dates varied by region.
- A lunisolar year starts at Chinese New Year. A regular month and a leap month with the same number are treated separately.
- The year range describes accepted input. The entire range has not been checked year by year against independent calendar tables.

## Developers

### Environment and dependencies

Pixi manages the runtime and development tools, including Designer and Linguist. Dependencies preferably come from conda-forge; `sxtwl` is installed from PyPI. See `pixi.toml` and `pixi.lock` for constraints and locked versions.

| Dependency | Version constraint | Source | Purpose |
| --- | --- | --- | --- |
| Python | `3.11.*` | conda | Python runtime |
| PySide6 | `>=6.8,<7` | conda | Qt interface and development tools |
| pip | `*` | conda | Python package management tool |
| sxtwl | `>=2.0.7,<3` | PyPI | Calendar conversion |
| PyInstaller | `>=6,<7` | conda | Windows desktop packaging |

### Project structure

<details>
<summary>Expand the project directory</summary>

```text
LunisolarCal/
├─ lunisolar_cal/
│  ├─ __init__.py       # Public API and version
│  ├─ __main__.py       # CLI entry point
│  ├─ core.py           # Validation and conversion
│  ├─ cli.py            # Command-line interface
│  ├─ gui.py            # Desktop interface and event handlers
│  ├─ formatting.py     # Date and error-message formatting
│  ├─ ui_converter.py   # Generated by uic
│  ├─ resources_rc.py   # Generated by rcc
│  ├─ i18n/
│  │  ├─ app_en.ts      # English translation source
│  │  └─ app_en.qm      # Compiled English translation
│  └─ ui/
│     ├─ lsconv.ui      # Designer form
│     ├─ resources.qrc  # Resource collection
│     └─ icons/         # Icons
├─ tests/
│  ├─ test_core.py      # Core tests
│  └─ test_cli.py       # CLI tests
├─ tools/
│  └─ build_windows.py  # Windows packaging script
├─ lunisolartr.py       # Compatibility CLI entry point
├─ README.md
├─ README.en.md
├─ LICENSE             # MIT license
├─ THIRD_PARTY_NOTICES.md
├─ THIRD_PARTY_NOTICES.en.md
├─ licenses/           # Third-party license texts
├─ pixi.toml
└─ pixi.lock
```

</details>

The core API and formatting module do not depend on Qt. The CLI and desktop interface share the same date validation and conversion logic. `MIN_INPUT_YEAR` and `MAX_INPUT_YEAR` in `core.py` define the accepted input range; the GUI uses the same limits during initialization. Check the conversion library's capabilities and boundary behavior before changing these limits.

### Editing the interface and icons

Start Designer, open `lunisolar_cal/ui/lsconv.ui`, and save your changes:

```powershell
pixi run designer
```

Generate Python modules from the form and resources:

| Source | Generated file |
| --- | --- |
| `lunisolar_cal/ui/resources.qrc` and its referenced icons | `lunisolar_cal/resources_rc.py` |
| `lunisolar_cal/ui/lsconv.ui` | `lunisolar_cal/ui_converter.py` |

Run from the project root:

```powershell
# Generate the icon resource module
pixi run pyside6-rcc lunisolar_cal/ui/resources.qrc -o lunisolar_cal/resources_rc.py

# Generate the form code
pixi run pyside6-uic --from-imports lunisolar_cal/ui/lsconv.ui -o lunisolar_cal/ui_converter.py
```

`--from-imports` uses a relative import for the resource module, matching the package structure. The generated form class is currently `Ui_LsConvWindow`.

- Run `pyside6-uic` again after editing the `.ui` file; run `pyside6-rcc` again after editing icons or the `.qrc` file.
- Regeneration overwrites the generated files. Keep event handlers and display logic in `gui.py`; edit the layout and appearance through Designer or the SVG source files.
- After editing handwritten Python code, save and restart the application.

### Maintaining interface translations

Simplified Chinese is the source language. English translations are stored in `lunisolar_cal/i18n/`. After changing translatable text, extract messages, edit translations, and compile them:

```powershell
# Extract messages from handwritten Python code and the Designer form
pixi run lupdate lunisolar_cal/core.py lunisolar_cal/formatting.py lunisolar_cal/gui.py lunisolar_cal/ui/lsconv.ui -ts lunisolar_cal/i18n/app_en.ts

# Complete translations in Linguist, mark them as finished, and save
pixi run linguist lunisolar_cal/i18n/app_en.ts

# Generate the translation file loaded at runtime
pixi run lrelease lunisolar_cal/i18n/app_en.ts -nounfinished -qm lunisolar_cal/i18n/app_en.qm
```

The `lupdate` task is configured to extract messages marked with `source_text`. Include the `.ui` source file, but leave out the generated `ui_converter.py` to avoid duplicate extraction.

Preserve placeholders such as `{version}`, `{year}`, and `{reason}`, along with HTML tags and links in rich text. Maintain both the `.ts` and `.qm` files; restart the application to load an updated `.qm`.

### Python API

Import conversion functions from `lunisolar_cal`:

```python
from lunisolar_cal import solar_to_lunisolar, lunisolar_to_solar

lunar = solar_to_lunisolar(2023, 3, 22)
# LunisolarDate(year=2023, month=2, day=1, is_leap=True)

solar = lunisolar_to_solar(2023, 2, 1, is_leap=True)
# SolarDate(year=2023, month=3, day=22)
```

Year, month, and day must be integers; `is_leap` must be a `bool`. Results are `NamedTuple` instances with `.year`, `.month`, and `.day` fields; lunisolar results also have `.is_leap`.

Conversion functions validate their input and raise `CalendarError`, a subclass of `ValueError`, for invalid input. Existing `except ValueError` handlers remain valid. Errors also retain `.template` and `.params` for translating messages in the interface. To validate a date without converting it, call `validate_solar_date()` or `validate_lunisolar_date()`.

When invoking the CLI from a script, successful results are written to standard output and error messages to standard error:

| Exit code | Meaning |
| --- | --- |
| `0` | Successful conversion or normal help display |
| `2` | Invalid arguments or date |
| `1` | Interactive input ended before completion |
| `130` | Input interrupted by the user |

### Tests

```powershell
pixi run test
```

Automated tests cover core conversion, date validation, error-message formatting, and CLI behavior. A successful run ends with `OK`. Also check the desktop interface manually: conversion in both directions, invalid-date messages, Today and Copy result, keyboard navigation, language switching, and the About and Licenses dialogs.

### Version maintenance

The software version is defined by `__version__` in `lunisolar_cal/__init__.py`, which the About dialog reads. `workspace.version` in `pixi.toml` is project metadata. Keep the two values in sync when releasing a new version.

### Windows packaging

Run on Windows using the project's Pixi environment:

```powershell
pixi run build
```

The script recompiles English translations, creates a desktop executable with its icon and version information, and copies both language versions of the documentation, the project license, and third-party license materials. Output:

```text
dist/
├─ LunisolarCal/
│  ├─ LunisolarCal.exe
│  ├─ _internal/          # Python, Qt, and other runtime libraries
│  ├─ licenses/           # License texts and supplied dependency build materials
│  ├─ BUNDLED_COMPONENTS.md
│  └─ ...                 # Chinese/English READMEs, third-party notices, LICENSE
├─ LunisolarCal-<version>-win64.zip
└─ LunisolarCal-<version>-win64.zip.sha256
```

`BUNDLED_COMPONENTS.md` records package versions, licenses, and materials for bundled native libraries, including source locations and patches supplied in their build recipes. Packaging requires the license materials and recipes in the current Conda package cache; missing materials cause an error. The build log is at `build/windows/pyinstaller.log`.

To test, extract the ZIP to a different directory, start the application, and check conversion, English language switching, icons, and the license viewer. For command-line use, follow the source-based instructions above.

## Other information

### License and third-party components

The project's own code, Qt forms, SVG icons, and documentation are licensed under the [MIT license](LICENSE), with the copyright notice `Copyright (c) 2026 AsahiKumo`.

Third-party dependencies retain their own license terms. See [Third-party components and licenses](THIRD_PARTY_NOTICES.en.md) ([简体中文](THIRD_PARTY_NOTICES.md)); full license texts are in [licenses](licenses/). When distributing a package containing Qt/PySide6 runtime libraries, include the license materials and source-code provision arrangements required for the components actually bundled.

### References

- [sxtwl project and usage](https://github.com/yuangu/sxtwl_cpp)
- [Generating Qt form code](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html)
- [Generating Qt resource modules](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html)
- [Using PyInstaller](https://pyinstaller.org/en/stable/usage.html)
