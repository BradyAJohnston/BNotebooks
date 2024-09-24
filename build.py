import glob
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import List, Union
import bpy
import shutil


def run_python(args: str):
    python = os.path.realpath(sys.executable)
    subprocess.run([python] + args.split(" "))


try:
    import tomlkit
except ImportError:
    run_python("-m pip install tomlkit".split(" "))
    import tomlkit

ADDON = "notebookconnector"

toml_path = f"{ADDON}/blender_manifest.toml"
whl_path = f"./{ADDON}wheels"


@dataclass
class Platform:
    pypi_suffix: str
    metadata: str


# tags for blender metadata
# platforms = ["windows-x64", "macos-arm64", "linux-x64", "windows-arm64", "macos-x64"]


windows_x64 = Platform(pypi_suffix="win_amd64", metadata="windows-x64")
linux_x64 = Platform(pypi_suffix="manylinux2014_x86_64", metadata="linux-x64")
macos_arm = Platform(pypi_suffix="macosx_12_0_arm64", metadata="macos-arm64")


required_packages = [
    # "pywinpty>=2",
    # "jupyter-server>=2.14",
    "pyzmq",
    "jupyterlab>=4",
]


build_platforms = [
    # windows_x64,
    # linux_x64,
    macos_arm
]


def remove_whls():
    for whl_file in glob.glob(os.path.join(whl_path, "*.whl")):
        os.remove(whl_file)


def download_whls(
    platforms: Union[Platform, List[Platform]],
    required_packages: List[str] = required_packages,
    python_version="3.11",
    clean: bool = True,
):
    if isinstance(platforms, Platform):
        platforms = [platforms]

    if clean:
        remove_whls()

    for platform in platforms:
        run_python(
            f"-m pip download {' '.join(required_packages)} --dest ./{ADDON}/wheels --only-binary=:all: --python-version={python_version} --platform={platform.pypi_suffix}"
        )


def get_whls(dir):
    return glob.glob(f"{dir}/*.whl")


def update_toml_whls(platforms):
    # Define the path for wheel files
    wheels_dir = f"{ADDON}/wheels"

    wheel_files = get_whls(wheels_dir)
    wheel_files.sort()

    # the package detection inside of blender, it currently misses the "universal"
    # builds for mac platforms, so we have to replace them with the `arm64` for apple
    # silicon macs. Should be able to do the same fo the intel macs but frankly I can't
    # be bothered trying to support them at the moment (or maybe ever)
    for whl in wheel_files:
        if "universal2" in whl:
            for platform in ["arm64"]:
                shutil.copy(whl, whl.replace("universal2", platform))

            os.remove(whl)

    wheel_files = get_whls(wheels_dir)

    # Packages to remove (currently empty so I haven't tried optimising build sizes at all)
    packages_to_remove = {}

    # Filter out unwanted wheel files
    to_remove = []
    to_keep = []
    for whl in wheel_files:
        if any(pkg in whl for pkg in packages_to_remove):
            to_remove.append(whl)
        else:
            to_keep.append(whl)

    # Remove the unwanted wheel files from the filesystem
    for whl in to_remove:
        os.remove(whl)

    # Load the TOML file
    with open(toml_path, "r") as file:
        manifest = tomlkit.parse(file.read())

    # Update the wheels list with the remaining wheel files
    manifest["wheels"] = [f"./wheels/{os.path.basename(whl)}" for whl in to_keep]

    # Simplify platform handling
    if not isinstance(platforms, list):
        platforms = [platforms]
    manifest["platforms"] = [p.metadata for p in platforms]

    # Write the updated TOML file
    with open(toml_path, "w") as file:
        file.write(
            tomlkit.dumps(manifest)
            .replace('["', '[\n\t"')
            .replace("\\\\", "/")
            .replace('", "', '",\n\t"')
            .replace('"]', '",\n]')
        )


def clean_files(suffix: str = ".blend1") -> None:
    pattern_to_remove = f"{ADDON}/**/*{suffix}"
    for blend1_file in glob.glob(pattern_to_remove, recursive=True):
        os.remove(blend1_file)


def build_extension(split: bool = True) -> None:
    for suffix in [".blend1", ".MNSession"]:
        clean_files(suffix=suffix)

    if split:
        subprocess.run(
            f"{bpy.app.binary_path} --command extension build"
            f" --split-platforms --source-dir {ADDON} --output-dir .".split(" ")
        )
    else:
        subprocess.run(
            f"{bpy.app.binary_path} --command extension build "
            f"--source-dir {ADDON} --output-dir .".split(" ")
        )


def build(platform) -> None:
    download_whls(platform)
    update_toml_whls(platform)
    build_extension()


def main():
    build(build_platforms)


if __name__ == "__main__":
    main()
