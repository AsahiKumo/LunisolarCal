# Third-party components and licenses

[简体中文](THIRD_PARTY_NOTICES.md) | English

This project uses the third-party software and color data listed below. Each component retains its original copyright notices and license terms; the project's [MIT license](LICENSE) does not change those terms. Full license texts are included in the [licenses](licenses/) directory.

The software versions below correspond to the current 64-bit Windows Pixi environment. See `pixi.lock` for exact versions. Software versions last checked: 2026-10-24; the Catppuccin palette source and check date are documented in its own section.

| Component | Version | Purpose | License and full text |
| --- | --- | --- | --- |
| sxtwl | 2.0.7 | Calendar calculations | [BSD-3-Clause](licenses/sxtwl-BSD-3-Clause.txt) |
| PySide6 / Shiboken6 | 6.11.2 | Python bindings for Qt | [LGPLv3](licenses/LGPL-3.0.txt) |
| Qt | 6.11.2 | GUI and icon rendering | [LGPLv3](licenses/LGPL-3.0.txt); see the module notes below |
| Python | 3.11.16 | Application runtime | [PSF and historical licenses](licenses/Python-LICENSE.txt) |
| pip | 26.2.2 | Package management tool in the environment | [MIT](licenses/pip-MIT.txt) |
| PyInstaller | 6.22.3 | Windows packaging tool | [GPLv2 with a bootloader exception](https://pyinstaller.org/en/stable/license.html) |
| FreeType | 2.14.3 | Qt font-rendering dependency | [FTL](licenses/freetype-FTL.txt) |
| Catppuccin palette | Palette data (2026-10-26) | Four custom color themes | [MIT](licenses/catppuccin-MIT.txt) |

## sxtwl

- Project: [yuangu/sxtwl_cpp](https://github.com/yuangu/sxtwl_cpp).
- Copyright notice: `Copyright (c) 2017-2022, 元谷`.
- License: [BSD-3-Clause](licenses/sxtwl-BSD-3-Clause.txt).

Thanks to 元谷, author of sxtwl_cpp, and 许剑伟, the original author of 寿星天文历.

The included license text was taken from the [upstream LICENSE](https://github.com/yuangu/sxtwl_cpp/blob/master/LICENSE). The 2.0.7 release metadata identifies the license as BSD, but the wheel and source distribution examined did not include a license file. The publicly available upstream text is therefore included with this provenance note.

## PySide6, Shiboken6, and Qt

Copyright belongs to The Qt Company Ltd. and the respective contributors. See each component's source code and accompanying materials for specific notices.

This project uses QtCore, QtGui, QtWidgets, and SVG icon support. The current PySide6 and Qt Conda packages identify their license as LGPL-3.0-only. Other Qt modules, development tools, and bundled third-party code may have different licenses and must be checked according to what is actually used.

The included [LGPLv3](licenses/LGPL-3.0.txt) text comes from the current Conda packages. The [companion GPLv3 text](licenses/GPL-3.0.txt) referenced by LGPLv3 is also included. GPLv3 is supplied alongside LGPLv3; the project's own license is stated in the root `LICENSE` file.

- [Qt for Python source](https://code.qt.io/cgit/pyside/pyside-setup.git/)
- [Qt source repositories](https://code.qt.io/cgit/qt/)
- [Qt for Python licensing](https://doc.qt.io/qtforpython-6/licenses.html)

## Python and pip

Python's copyright belongs to the Python Software Foundation and the rights holders named in its accompanying historical licenses. [Python-LICENSE.txt](licenses/Python-LICENSE.txt) preserves the complete license text supplied by the current Python Conda package. See [Python licensing](https://docs.python.org/3.11/license.html).

pip's copyright notice is `Copyright (c) 2008-present The pip developers (see AUTHORS.txt file)`. [pip-MIT.txt](licenses/pip-MIT.txt) preserves the license text supplied by the current pip Conda package. The author list is available in [pip AUTHORS.txt](https://github.com/pypa/pip/blob/main/AUTHORS.txt). pip is used for environment management; the application itself does not import it.

## FreeType

This software is based in part on the work of the FreeType Team. Bundled FreeType 2.14.3 uses its FTL license option. The [license text](licenses/freetype-FTL.txt) comes from [FTL.TXT in the corresponding upstream release](https://github.com/freetype/freetype/blob/VER-2-14-3/docs/FTL.TXT), supplementing the license text omitted from the current Conda runtime subpackage.

## Catppuccin palette

This project uses the Latte, Frappé, Macchiato, and Mocha colors from the [official Catppuccin palette](https://github.com/catppuccin/palette/blob/main/palette.json), checked on 2026-10-26. The Qt theme-switching and widget-color implementation is written for this project.

- Copyright notice: `Copyright (c) 2021 Catppuccin`.
- License: [MIT text](licenses/catppuccin-MIT.txt), taken from the [official palette repository's LICENSE](https://github.com/catppuccin/palette/blob/main/LICENSE).
- Color roles follow the [official style guide](https://github.com/catppuccin/catppuccin/blob/main/docs/style-guide.md).

## Distribution notes

PyInstaller's bootloader exception allows a generated application to use its own license, subject to the licenses of the application's dependencies. The Windows build script also generates `BUNDLED_COMPONENTS.md` to record the package owners of detected bundled native libraries, and copies their supplied license texts and build recipes into `licenses/bundled/`.

When sharing the project source, retain the relevant copyright notices, third-party notices, and license texts. Review the versions and licenses here when updating dependencies.

If distributing an executable or installer containing Qt/PySide6 runtime libraries, fulfill the applicable license obligations for the components actually bundled. These include providing notices and license texts, the corresponding library source code or a compliant arrangement for supplying it, preserving users' rights to replace or relink modified libraries and debug those modifications, and providing any applicable installation information. See [Qt's LGPL obligations](https://www.qt.io/development/open-source-lgpl-obligations).

This document lists the main dependencies. Add notices for other dependencies and Qt plugins included in a distribution according to its actual contents.
