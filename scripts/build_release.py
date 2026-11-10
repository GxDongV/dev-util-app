"""Build all Windows x64 release artifacts without overwriting other variants."""

import argparse
import hashlib
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def find_iscc(explicit=None):
    candidates = [explicit, os.environ.get("ISCC"), shutil.which("ISCC.exe")]
    candidates += [
        str(Path(os.environ.get(base, "C:/Program Files")) / folder / "ISCC.exe")
        for base in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")
        for folder in ("Inno Setup 7", "Inno Setup 6", "Programs/Inno Setup 6")
    ]
    candidates.append(str(ROOT / "build/tools/inno/ISCC.exe"))
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise FileNotFoundError("Install Inno Setup 6.3+ or pass --iscc PATH/ISCC.exe")


def build_variant(kind, version):
    dist = ROOT / "dist" / kind
    work = ROOT / "build/release" / kind
    work.mkdir(parents=True, exist_ok=True)
    version_tuple = tuple(map(int, version.split("."))) + (0,)
    version_file = work / "version_info.txt"
    version_file.write_text(
        "VSVersionInfo("
        f"ffi=FixedFileInfo(filevers={version_tuple!r}, prodvers={version_tuple!r}, "
        "mask=0x3f, flags=0, OS=0x40004, fileType=0x1, subtype=0, date=(0, 0)), "
        "kids=[StringFileInfo([StringTable('040904B0', ["
        "StringStruct('CompanyName', 'GxDongV'), "
        "StringStruct('FileDescription', 'DevUtilsApp developer utilities'), "
        f"StringStruct('FileVersion', '{version}'), "
        "StringStruct('ProductName', 'DevUtilsApp'), "
        f"StringStruct('ProductVersion', '{version}'), "
        "StringStruct('OriginalFilename', 'DevUtilsApp.exe')])]), "
        "VarFileInfo([VarStruct('Translation', [1033, 1200])])])",
        encoding="utf-8",
    )
    command = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--windowed", "--onefile" if kind == "single" else "--onedir",
        "--name", "DevUtilsApp", "--distpath", str(dist),
        "--workpath", str(work), "--specpath", str(work),
        "--paths", str(ROOT), "--icon", str(ROOT / "assets/app_icon.ico"),
        "--version-file", str(version_file), "--collect-all", "qdarkstyle",
        "--add-data", f"{ROOT / 'assets'}{os.pathsep}assets",
        str(ROOT / "src/main.py"),
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    return dist / ("DevUtilsApp.exe" if kind == "single" else "DevUtilsApp")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iscc", help="Path to the Inno Setup compiler")
    args = parser.parse_args()
    if sys.platform != "win32" or platform.architecture()[0] != "64bit":
        parser.error("Use 64-bit Python on Windows to build Windows x64 releases")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if len(version.split(".")) != 3 or not all(p.isdecimal() for p in version.split(".")):
        parser.error("VERSION must contain a three-part version such as 0.0.2")
    iscc = find_iscc(args.iscc)
    output = ROOT / "release"
    output.mkdir(exist_ok=True)
    prefix = f"DevUtilsApp-{version}-windows-x64"
    portable = build_variant("portable", version)
    for filename in ("LICENSE", "readme.md", "VERSION"):
        shutil.copy2(ROOT / filename, portable / filename)
    single = build_variant("single", version)
    single_output = output / f"{prefix}-single.exe"
    shutil.copy2(single, single_output)
    zip_output = output / f"{prefix}-portable.zip"
    with zipfile.ZipFile(zip_output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(portable.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(portable.parent))
    subprocess.run([
        iscc, f"/DAppVersion={version}", f"/DSourceDir={portable}",
        f"/DReleaseDir={output}", str(ROOT / "setup.iss"),
    ], cwd=ROOT, check=True)
    artifacts = [single_output, zip_output, output / f"{prefix}-setup.exe"]
    checksum_lines = []
    for artifact in artifacts:
        with artifact.open("rb") as stream:
            hasher = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(chunk)
            digest = hasher.hexdigest()
        checksum_lines.append(f"{digest}  {artifact.name}\n")
        print(f"{artifact.name}: {artifact.stat().st_size:,} bytes", flush=True)
    (output / "SHA256SUMS.txt").write_text("".join(checksum_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
