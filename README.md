# 公农历转换工具

简体中文 | [English](README.en.md)

A solar-lunisolar calendar converter with a Qt desktop interface and a command-line interface. It supports leap months, date validation, and a Chinese/English desktop interface. See the [English documentation](README.en.md) for installation and usage.

基于 `sxtwl` 的公历、农历双向转换工具，提供 Qt 桌面窗口、命令行和 Python 调用接口，支持闰月输入与日期校验。

> 应该没有人会用我的这个东西吧……

- 桌面界面支持简体中文、英文和跟随系统语言。
- 支持填入今天、中文农历表示、复制结果和键盘快捷键。
- 可在“关于”窗口查看版本、项目地址及本地许可说明。

文档导航：[使用者](#使用者) · [开发者](#开发者) · [其他信息](#其他信息)

## 使用者

### 首次运行

Windows 64 位桌面包可解压整个 ZIP 后，双击其中的 `LunisolarCal.exe` 启动，无需安装 Python 或 Pixi。请保留旁边的 `_internal`、`licenses` 及说明文件；移动或分享时保留整个文件夹。

从源码运行时，先安装 [Pixi](https://pixi.prefix.dev/latest/installation/)，再在项目根目录（`pixi.toml` 所在目录）打开 PowerShell，安装运行环境：

```powershell
pixi install --locked
```

下文所有命令均在项目根目录执行。

### 桌面窗口

```powershell
pixi run python -m lunisolar_cal.gui
```

1. 选择输入历法：公历或农历。
2. 填写年、月、日；输入农历闰月时勾选“闰月”。
3. 公历转农历时，可选择“中文农历表示”，以“正月”“闰二月”“初一”等名称显示结果。
4. 点击“转换”，查看另一种历法的日期。

公历输入时，闰月选项自动禁用；农历输入时，“中文农历表示”选项禁用。无效日期会在结果区域显示原因。修改输入或界面语言后，结果恢复为“等待转换”，再次转换即可计算。

常用操作：

| 操作 | 说明 |
| --- | --- |
| 今天 | 保留当前输入历法，填入今天对应的日期并转换 |
| 复制结果 | 复制最近一次成功转换的结果；输入变化或转换失败后禁用 |
| 界面语言 | 选择简体中文、英文或跟随系统；中文农历表示可独立选择 |
| 关于 → 许可说明 | 查看项目信息、第三方组件说明及许可原文；Markdown 说明支持格式化显示 |

“跟随系统”按系统界面语言偏好匹配中英文。当前所有中文语言变体（含繁体中文地区）均使用简体中文；未匹配到支持的语言时回退英文。

| 快捷键 | 操作 |
| --- | --- |
| `Enter` | 转换 |
| `Alt+T` | 填入今天并转换 |
| `Ctrl+Shift+C` | 复制有效结果 |
| `Tab` / `Shift+Tab` | 在控件之间移动焦点 |

结果区域的文字也可以直接选中并复制。

### 命令行

直接指定日期：

```powershell
# 公历 2024-02-10 → 农历 2024 年 1 月 1 日
pixi run cal s 2024 2 10

# 农历 2023 年普通二月初一 → 公历 2023-02-20
pixi run cal ls 2023 2 1

# 农历 2023 年闰二月初一 → 公历 2023-03-22
pixi run cal ls 2023 2 1 -l
```

`s` 表示输入公历，`ls` 表示输入农历，也可以分别写成 `-s`、`-ls`。农历默认按普通月份处理；`-l` 或 `--leap` 表示输入的是闰月。

也可以不带参数，按提示逐项输入：

```powershell
pixi run cal
```

查看参数说明：

```powershell
pixi run cal --help
pixi run cal ls --help
```

命令行的提示、帮助和输出目前使用中文；桌面窗口中的语言选择只作用于 GUI。

### 历法范围与约定

- **输入年份为 `1～9999`**。跨年转换的输出可能为农历 0 年或公历 10000 年，这类结果超出当前可输入范围。
- 公历在 **1582-10-04 及以前按儒略历**解释，**1582-10-15 起按格里高利历**解释；1582-10-05 至 14 日属于改历缺口，不能输入。这是程序采用的固定改历规则，与各地区实际采用新历的时间可能不同。
- 农历以春节划分年份，普通月份与同名闰月分别处理。
- 年份范围表示程序接受的输入范围；整个范围尚未逐年通过独立历表核对。

## 开发者

### 开发说明

本项目开发过程中使用了 OpenAI Codex 辅助编程、调试、文档整理和 UI 图标制作。

### 环境与依赖

运行环境与开发工具（包括 Designer、Linguist）统一由 Pixi 管理，依赖优先使用 conda-forge，`sxtwl` 通过 PyPI 安装。具体约束与锁定版本见 `pixi.toml` 和 `pixi.lock`。

| 依赖 | 版本约束 | 来源 | 用途 |
| --- | --- | --- | --- |
| Python | `3.11.*` | conda | Python 运行时 |
| PySide6 | `>=6.8,<7` | conda | Qt 窗口与开发工具 |
| pip | `*` | conda | Python 包管理工具 |
| sxtwl | `>=2.0.7,<3` | PyPI | 历法转换 |
| PyInstaller | `>=6,<7` | conda | 生成 Windows 桌面包 |

### 项目代码结构

```text
LunisolarCal/
├─ lunisolar_cal/
│  ├─ __init__.py       # 公共接口与版本号
│  ├─ __main__.py       # 命令行入口
│  ├─ core.py           # 校验与转换
│  ├─ cli.py            # 命令行
│  ├─ gui.py            # 桌面界面与事件处理
│  ├─ formatting.py     # 日期格式与错误提示格式化
│  ├─ ui_converter.py   # 由 uic 生成
│  ├─ resources_rc.py   # 由 rcc 生成
│  ├─ i18n/
│  │  ├─ app_en.ts      # 英文翻译源文件
│  │  └─ app_en.qm      # 编译后的英文翻译
│  └─ ui/
│     ├─ lsconv.ui      # Designer UI
│     ├─ resources.qrc  # 资源清单
│     └─ icons/         # 图标
├─ tests/
│  ├─ test_core.py      # 核心测试
│  └─ test_cli.py       # 命令行测试
├─ tools/
│  └─ build_windows.py  # Windows 打包脚本
├─ lunisolartr.py       # 兼容命令行入口
├─ README.md
├─ README.en.md
├─ LICENSE             # MIT 许可证
├─ THIRD_PARTY_NOTICES.md
├─ THIRD_PARTY_NOTICES.en.md
├─ licenses/           # 第三方许可
├─ pixi.toml
└─ pixi.lock
```

核心接口与格式化模块不依赖 Qt，命令行和桌面窗口共用同一套日期校验与转换逻辑。输入年份上下限由 `core.py` 的 `MIN_INPUT_YEAR`、`MAX_INPUT_YEAR` 定义，GUI 在初始化时也使用这个范围。调整范围前，应核对转换库的能力和边界行为。

### 修改界面与图标

启动 Designer，打开 `lunisolar_cal/ui/lsconv.ui`，编辑后保存：

```powershell
pixi run designer
```

窗体和资源文件分别生成对应的 Python 模块：

| 源文件 | 生成文件 |
| --- | --- |
| `lunisolar_cal/ui/resources.qrc` 及其引用的图标 | `lunisolar_cal/resources_rc.py` |
| `lunisolar_cal/ui/lsconv.ui` | `lunisolar_cal/ui_converter.py` |

在项目根目录执行：

```powershell
# 生成图标资源模块
pixi run pyside6-rcc lunisolar_cal/ui/resources.qrc -o lunisolar_cal/resources_rc.py

# 生成窗体代码
pixi run pyside6-uic --from-imports lunisolar_cal/ui/lsconv.ui -o lunisolar_cal/ui_converter.py
```

`--from-imports` 使窗体代码通过相对导入加载资源模块，适配当前包结构。当前生成的窗体类为 `Ui_LsConvWindow`。

- 修改 `.ui` 后重新运行 `pyside6-uic`；修改图标或 `.qrc` 后重新运行 `pyside6-rcc`。
- 生成文件会被覆盖。窗口事件和显示逻辑写在 `gui.py`，图形样式通过 Designer 或 SVG 源文件维护。
- 修改手写 Python 代码后，保存并重新启动窗口即可。

### 维护界面翻译

界面以简体中文为源语言，英文翻译位于 `lunisolar_cal/i18n/`。修改可翻译文字后，依次提取文字、编辑翻译并编译：

```powershell
# 从手写 Python 代码和 Designer 窗体提取文字
pixi run lupdate lunisolar_cal/core.py lunisolar_cal/formatting.py lunisolar_cal/gui.py lunisolar_cal/ui/lsconv.ui -ts lunisolar_cal/i18n/app_en.ts

# 在 Linguist 中补充翻译，标记完成并保存
pixi run linguist lunisolar_cal/i18n/app_en.ts

# 生成运行时加载的翻译文件
pixi run lrelease lunisolar_cal/i18n/app_en.ts -nounfinished -qm lunisolar_cal/i18n/app_en.qm
```

`lupdate` 任务已配置 `source_text` 标记的提取规则。提取范围包含 `.ui` 源文件，不加入生成的 `ui_converter.py`，以免重复提取。

翻译时保留 `{version}`、`{year}`、`{reason}` 等占位符，以及富文本中的 HTML 标签和链接。`.ts`、`.qm` 文件需要一并维护；重新启动程序后加载新的 `.qm`。

### 程序接口

从 `lunisolar_cal` 导入转换函数：

```python
from lunisolar_cal import solar_to_lunisolar, lunisolar_to_solar

lunar = solar_to_lunisolar(2023, 3, 22)
# LunisolarDate(year=2023, month=2, day=1, is_leap=True)

solar = lunisolar_to_solar(2023, 2, 1, is_leap=True)
# SolarDate(year=2023, month=3, day=22)
```

年月日参数必须为整数，`is_leap` 必须为 bool。结果为带字段名的 `NamedTuple`，可以通过 `.year`、`.month`、`.day` 读取；农历结果还包含 `.is_leap`。

转换函数已包含日期校验，无效输入抛出 `CalendarError`（`ValueError` 的子类），现有的 `except ValueError` 仍然适用。异常还保留 `.template` 和 `.params`，供界面翻译错误提示。需要单独校验时，可调用 `validate_solar_date()` 或 `validate_lunisolar_date()`。

脚本调用命令行时，成功结果写入标准输出，错误原因写入标准错误：

| 退出码 | 含义 |
| --- | --- |
| `0` | 转换成功或正常显示帮助 |
| `2` | 参数或日期无效 |
| `1` | 交互输入提前结束 |
| `130` | 用户中断输入 |

### 测试

```powershell
pixi run test
```

自动化测试覆盖核心转换、日期校验、错误提示格式化和命令行行为，全部通过时显示 `OK`。界面还应手动核对双向转换、错误提示、今天与复制按钮、键盘操作、语言切换以及关于和许可窗口。

### 版本维护

软件版本号位于 `lunisolar_cal/__init__.py` 的 `__version__`，关于窗口从这里读取；`pixi.toml` 的 `workspace.version` 是项目元数据。发布新版本时保持两处一致。

### Windows 打包

在 Windows 上使用项目的 Pixi 环境运行：

```powershell
pixi run build
```

脚本重新编译英文翻译，生成带图标和版本信息的桌面程序，并复制中英文说明、项目许可和第三方许可材料。输出位于：

```text
dist/
├─ LunisolarCal/
│  ├─ LunisolarCal.exe
│  ├─ _internal/          # Python、Qt 和其他运行库
│  ├─ licenses/           # 许可文本及依赖包提供的构建材料
│  ├─ BUNDLED_COMPONENTS.md
│  └─ ...                 # 中英文 README 与第三方说明、LICENSE
├─ LunisolarCal-<版本号>-win64.zip
└─ LunisolarCal-<版本号>-win64.zip.sha256
```

`BUNDLED_COMPONENTS.md` 记录随包原生库对应的包版本、许可及材料位置，包含构建包提供的源码地址与补丁信息。打包需要当前 Conda 包缓存中的许可和构建配方；材料缺失时脚本会报错。日志位于 `build/windows/pyinstaller.log`。

测试时，先将 ZIP 解压到另一个目录，再启动桌面程序，检查转换、英文切换、图标和许可查看。命令行调用仍使用前面的源码环境和 `pixi run cal`。

## 其他信息

### 许可证与第三方组件

本项目自有代码、Qt 窗体、SVG 图标和文档采用 [MIT 许可证](LICENSE)，版权署名为 `Copyright (c) 2026 AsahiKumo`。

第三方依赖保留各自的许可条件，详情见 [第三方组件与许可](THIRD_PARTY_NOTICES.md)（[English](THIRD_PARTY_NOTICES.en.md)），许可全文收录于 [licenses](licenses/) 目录。分发包含 Qt/PySide6 运行库的安装包时，还应按实际随包组件补齐相应许可材料和源码提供安排。

### 参考资料

- [sxtwl 项目与使用说明](https://github.com/yuangu/sxtwl_cpp)
- [Qt 窗体代码生成](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html)
- [Qt 资源模块生成](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html)
- [PyInstaller 使用说明](https://pyinstaller.org/en/stable/usage.html)
