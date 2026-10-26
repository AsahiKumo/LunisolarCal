"""Build the Windows desktop bundle with the active Pixi environment."""

import ast
import hashlib
from importlib.metadata import version as package_version
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lunisolar_cal import __version__


NAME = "LunisolarCal"
BUILD = ROOT / "build" / "windows"
DIST = ROOT / "dist"
DOCS = (
    "README.md", "README.en.md", "LICENSE",
    "THIRD_PARTY_NOTICES.md", "THIRD_PARTY_NOTICES.en.md",
)


def windows_version(version):
    """Keep the display version while using numeric Windows version fields."""
    match = re.fullmatch(r"(\d+(?:\.\d+){0,3})((?:a|b|rc|pre)\d+)?", version)
    if match is None:
        raise ValueError("Expected a release such as 1.3.1 or a prerelease such as 1.3.1pre1.")
    numbers = tuple(int(part) for part in match.group(1).split("."))
    if any(part > 65535 for part in numbers):
        raise ValueError("Windows version components must be between 0 and 65535.")
    numbers += (0,) * (4 - len(numbers))
    flags = 0x2 if match.group(2) else 0  # VS_FF_PRERELEASE
    return numbers, flags


def make_assets():
    """Generate the entry point, Windows icon, and executable version metadata."""
    from PySide6.QtGui import QGuiApplication, QIcon
    from PyInstaller.utils.win32.versioninfo import (
        FixedFileInfo, StringFileInfo, StringStruct, StringTable,
        VarFileInfo, VarStruct, VSVersionInfo,
    )

    app = QGuiApplication.instance() or QGuiApplication([])
    icon = BUILD / "calendar.ico"
    svg = ROOT / "lunisolar_cal" / "ui" / "icons" / "calendar.svg"
    if not QIcon(str(svg)).pixmap(256, 256).save(str(icon), "ICO"):
        raise RuntimeError("Unable to generate the Windows icon.")

    version, flags = windows_version(__version__)
    metadata = VSVersionInfo(
        ffi=FixedFileInfo(filevers=version, prodvers=version, flags=flags, fileType=1),
        kids=[
            StringFileInfo([StringTable("040904B0", [
                StringStruct("CompanyName", "AsahiKumo"),
                StringStruct("FileDescription", "Solar-Lunisolar Calendar Converter"),
                StringStruct("FileVersion", __version__),
                StringStruct("ProductName", NAME),
                StringStruct("ProductVersion", __version__),
                StringStruct("OriginalFilename", NAME + ".exe"),
                StringStruct("LegalCopyright", "Copyright (c) 2026 AsahiKumo"),
            ])]),
            VarFileInfo([VarStruct("Translation", [0x409, 1200])]),
        ],
    )
    version_file = BUILD / "version.txt"
    version_file.write_text(str(metadata), encoding="utf-8")
    entry = BUILD / "desktop.py"
    entry.write_text(
        "import sys\n"
        "from PySide6.QtWidgets import QApplication\n"
        "from lunisolar_cal.gui import LsConvWindow\n"
        "app = QApplication(sys.argv)\n"
        "window = LsConvWindow()\n"
        "window.show()\n"
        "sys.exit(app.exec())\n",
        encoding="utf-8",
    )
    return app, entry, icon, version_file


def copy_component_materials(bundle):
    """Record owners of collected native libraries and copy their supplied materials."""
    prefix = Path(sys.prefix).resolve()
    records = {}
    owners = {}
    for record in (prefix / "conda-meta").glob("*.json"):
        data = json.loads(record.read_text(encoding="utf-8"))
        records[data["name"]] = data
        for filename in data.get("files", []):
            owners[str((prefix / filename).resolve()).casefold()] = data["name"]

    toc_file = BUILD / "work" / NAME / "COLLECT-00.toc"
    entries = ast.literal_eval(toc_file.read_text(encoding="utf-8"))[0]
    used = {"pyinstaller"}
    unmatched = []
    for destination, source, kind in entries:
        if kind not in {"BINARY", "EXTENSION"}:
            continue
        path = Path(source).resolve()
        owner = owners.get(str(path).casefold())
        if owner:
            used.add(owner)
        elif path.name.lower().startswith("_sxtwl"):
            continue
        elif path.is_relative_to(prefix):
            unmatched.append(destination)
    if unmatched:
        raise RuntimeError("Unidentified bundled libraries: " + ", ".join(unmatched))

    lines = [
        "# Bundled components", "",
        f"Application version: {__version__}", "",
        "Generated from PyInstaller's collected native files and Conda package records.",
        "The materials below are supplied by the binary package maintainers; the",
        "build recipes record upstream source archives and downstream patches.", "",
        "| Component | Version | License | Materials |",
        "| --- | --- | --- | --- |",
    ]
    for name in sorted(used):
        record = records[name]
        cache = Path(record["link"]["source"]) / "info"
        target = bundle / "licenses" / "bundled" / name
        target.mkdir(parents=True, exist_ok=True)
        for folder in ("licenses", "recipe"):
            source = cache / folder
            if source.is_dir():
                shutil.copytree(source, target / folder, dirs_exist_ok=True)
        if name == "libfreetype6" and record["version"] == "2.14.3":
            # This split Conda output omits license files; use its upstream FTL option.
            (target / "licenses").mkdir(exist_ok=True)
            shutil.copy2(ROOT / "licenses/freetype-FTL.txt", target / "licenses/FTL.TXT")
        if not (target / "licenses").exists():
            raise FileNotFoundError(f"Package license materials are unavailable: {name}")
        metadata = {key: record.get(key) for key in (
            "name", "version", "build", "license", "url", "sha256",
        )}
        (target / "package.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
        )
        selected_license = "FTL" if name == "libfreetype6" else record.get("license", "")
        lines.append(
            f"| {name} | {record['version']} | {selected_license} | "
            f"[licenses and recipe](licenses/bundled/{name}/) |"
        )
    lines += [
        f"| sxtwl | {package_version('sxtwl')} | BSD-3-Clause | [license](licenses/sxtwl-BSD-3-Clause.txt) |",
        "", "See THIRD_PARTY_NOTICES.md or THIRD_PARTY_NOTICES.en.md for component notes.",
        "Python's complete license and the LGPL/GPL texts are also in licenses/.", "",
    ]
    (bundle / "BUNDLED_COMPONENTS.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    if sys.platform != "win32":
        raise SystemExit("Run this task on Windows with the project's Pixi environment.")
    config = tomllib.loads((ROOT / "pixi.toml").read_text(encoding="utf-8"))
    if config["workspace"]["version"] != __version__:
        raise SystemExit("Keep workspace.version and lunisolar_cal.__version__ in sync.")
    for path in (BUILD, DIST, DIST / NAME):
        if path.resolve() != path:
            raise SystemExit(f"Build output cannot be redirected by a symlink or junction: {path}")
    BUILD.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(exist_ok=True)

    qt_bin = Path(sys.prefix) / "Library" / "lib" / "qt6" / "bin"
    subprocess.run([
        str(qt_bin / "lrelease.exe"), str(ROOT / "lunisolar_cal/i18n/app_en.ts"),
        "-nounfinished", "-qm", str(ROOT / "lunisolar_cal/i18n/app_en.qm"),
    ], check=True)
    app, entry, icon, version_file = make_assets()
    command = [
        sys.executable, "-B", "-m", "PyInstaller", "--onedir", "--windowed",
        "--noconfirm", "--clean", "--noupx", "--name", NAME,
        "--paths", str(ROOT), "--distpath", str(DIST),
        "--workpath", str(BUILD / "work"), "--specpath", str(BUILD),
        "--icon", str(icon), "--version-file", str(version_file),
        "--add-data", f"{ROOT / 'lunisolar_cal/i18n/app_en.qm'}:lunisolar_cal/i18n",
        # Collect the Conda-owned CRT instead of older copies in Shiboken's directory.
        "--add-binary", f"{Path(sys.prefix) / 'Library/bin/vcruntime140.dll'}:shiboken6",
        "--add-binary", f"{Path(sys.prefix) / 'Library/bin/vcruntime140_1.dll'}:shiboken6",
        str(entry),
    ]
    env = os.environ.copy()
    env["PYINSTALLER_CONFIG_DIR"] = str(BUILD / "cache")
    log = BUILD / "pyinstaller.log"
    print(f"Building {NAME} {__version__}; log: {log}", flush=True)
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=ROOT, env=env, stdout=output, stderr=subprocess.STDOUT)
    if result.returncode:
        print("\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-50:]))
        raise SystemExit(result.returncode)

    bundle = DIST / NAME
    for filename in DOCS:
        shutil.copy2(ROOT / filename, bundle / filename)
    shutil.copytree(ROOT / "licenses", bundle / "licenses", dirs_exist_ok=True)
    shutil.copytree(ROOT / "docs" / "images", bundle / "docs" / "images", dirs_exist_ok=True)
    copy_component_materials(bundle)
    archive = Path(shutil.make_archive(
        str(DIST / f"{NAME}-{__version__}-win64"), "zip", root_dir=DIST, base_dir=NAME,
    ))
    with archive.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    print(f"Executable: {bundle / (NAME + '.exe')}")
    print(f"Archive: {archive}")


if __name__ == "__main__":
    main()
