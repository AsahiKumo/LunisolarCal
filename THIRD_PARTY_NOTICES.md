# 第三方组件与许可

简体中文 | [English](THIRD_PARTY_NOTICES.en.md)

本项目使用以下第三方软件与配色数据。各组件保留原作者的版权和许可条件，项目自身的 [MIT 许可证](LICENSE) 不改变这些条件。许可原文收录于 [licenses](licenses/) 目录。

以下软件版本对应当前 Windows 64 位 Pixi 环境，具体版本见 `pixi.lock`。软件版本核对日期：2026-10-24；Catppuccin 色板的来源与核对日期见对应小节。

| 组件 | 版本 | 用途 | 许可与原文 |
| --- | --- | --- | --- |
| sxtwl | 2.0.7 | 历法计算 | [BSD-3-Clause](licenses/sxtwl-BSD-3-Clause.txt) |
| PySide6 / Shiboken6 | 6.11.2 | Qt 的 Python 绑定 | [LGPLv3](licenses/LGPL-3.0.txt) |
| Qt | 6.11.2 | 窗口和图标显示 | [LGPLv3](licenses/LGPL-3.0.txt)，具体模块见下文 |
| Python | 3.11.16 | 程序运行时 | [PSF 及历史许可](licenses/Python-LICENSE.txt) |
| pip | 26.2.2 | 环境中的包管理工具 | [MIT](licenses/pip-MIT.txt) |
| PyInstaller | 6.22.3 | Windows 打包工具 | [GPLv2 及引导程序例外](https://pyinstaller.org/en/stable/license.html) |
| FreeType | 2.14.3 | Qt 字体渲染依赖 | [FTL](licenses/freetype-FTL.txt) |
| Catppuccin 色板 | 色板数据（2026-10-26） | 四套自定义主题配色 | [MIT](licenses/catppuccin-MIT.txt) |

## sxtwl

- 项目：[yuangu/sxtwl_cpp](https://github.com/yuangu/sxtwl_cpp)。
- 版权声明：`Copyright (c) 2017-2022, 元谷`。
- 许可：[BSD-3-Clause](licenses/sxtwl-BSD-3-Clause.txt)。

感谢 sxtwl_cpp 作者元谷，以及寿星天文历原作者许剑伟。

随附许可文本取自[上游 LICENSE](https://github.com/yuangu/sxtwl_cpp/blob/master/LICENSE)。2.0.7 的发行元数据标为 BSD，但已核对的 wheel 和源码发行包未附许可文件，因此这里保留上游公开文本作为来源说明。

## PySide6、Shiboken6 与 Qt

版权属于 The Qt Company Ltd. 及相关贡献者，具体声明见各组件的源码和随附材料。

本项目使用 QtCore、QtGui、QtWidgets 及 SVG 图标支持。当前环境中的 PySide6 和 Qt Conda 包标注为 LGPL-3.0-only；Qt 的其他模块、开发工具及内含的第三方代码可能采用不同许可，需按实际使用内容核对。

随附的 [LGPLv3](licenses/LGPL-3.0.txt) 原文来自当前 Conda 包；同时提供其引用的 [GPLv3 配套文本](licenses/GPL-3.0.txt)。这份 GPLv3 文本随 LGPLv3 一并收录，项目自身采用的许可仍见根目录 `LICENSE`。

- [Qt for Python 源码](https://code.qt.io/cgit/pyside/pyside-setup.git/)
- [Qt 源码仓库](https://code.qt.io/cgit/qt/)
- [Qt for Python 许可说明](https://doc.qt.io/qtforpython-6/licenses.html)

## Python 与 pip

Python 的版权属于 Python Software Foundation 及随附历史许可中列明的权利人。[Python-LICENSE.txt](licenses/Python-LICENSE.txt) 保留当前 Python Conda 包提供的完整许可文本。参见 [Python 许可说明](https://docs.python.org/3.11/license.html)。

pip 的版权声明为 `Copyright (c) 2008-present The pip developers (see AUTHORS.txt file)`。[pip-MIT.txt](licenses/pip-MIT.txt) 保留当前 pip Conda 包提供的许可文本，作者名单见 [pip AUTHORS.txt](https://github.com/pypa/pip/blob/main/AUTHORS.txt)。pip 用于环境管理，程序本身不导入它。

## FreeType

本软件部分基于 FreeType 团队的工作。随包的 FreeType 2.14.3 使用其 FTL 许可选项；[许可原文](licenses/freetype-FTL.txt) 取自[该版本上游的 FTL.TXT](https://github.com/freetype/freetype/blob/VER-2-14-3/docs/FTL.TXT)，用于补齐当前 Conda 运行库子包未附带的许可文本。

## Catppuccin 色板

本项目使用 [Catppuccin 官方色板](https://github.com/catppuccin/palette/blob/main/palette.json)中的 Latte、Frappé、Macchiato 和 Mocha 色值，核对日期为 2026-10-26。Qt 主题切换和控件配色代码由本项目实现。

- 版权声明：`Copyright (c) 2021 Catppuccin`。
- 许可：[MIT 原文](licenses/catppuccin-MIT.txt)，取自[官方色板仓库 LICENSE](https://github.com/catppuccin/palette/blob/main/LICENSE)。
- 配色用途参考[官方风格指南](https://github.com/catppuccin/catppuccin/blob/main/docs/style-guide.md)。

## 分发说明

PyInstaller 的引导程序例外允许生成的应用采用自身的许可，仍需遵守应用依赖的许可条件。Windows 打包脚本会另行生成 `BUNDLED_COMPONENTS.md`，记录检测到的随包原生库所属包，并将包内提供的许可和构建配方收录到 `licenses/bundled/`。

分享项目源码时，请保留相关版权声明、第三方说明和许可文本。更新依赖时，也应同步复核这里的版本和许可。

如果分发包含 Qt/PySide6 运行库的可执行程序或安装包，还需根据实际随包组件履行相应许可义务，包括提供声明与许可文本、对应库源码或合规的源码提供安排，以及保障用户替换或重新链接修改后的库、调试修改及适用的安装信息等权利。详见 [Qt 的 LGPL 义务说明](https://www.qt.io/development/open-source-lgpl-obligations)。

本文件列出主要依赖。安装包中随附的其他依赖和 Qt 插件，应按实际内容补充声明。
