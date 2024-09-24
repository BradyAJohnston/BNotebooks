import json
import os
import pathlib
import shutil
import subprocess
import sys
import textwrap
import bpy
import platform
import runpy
import io


_is_apple_silicon = (sys.platform == "darwin") and ("arm" in platform.machine())


EXTENSIONS_PATH = pathlib.Path(__file__).parent.parent.parent
EXTENSIONS_SITE_PACKAGES = EXTENSIONS_PATH / ".local/lib/python3.11/site-packages/"


def get_kernel_path(kernel_dir):
    kernel_path = None
    if kernel_dir:
        kernel_path = pathlib.Path(kernel_dir)
    else:
        try:
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            old_argv = sys.argv.copy()
            sys.argv = ["jupyter", "--data-dir"]
            runpy.run_module("jupyter", run_name="__main__")
            data_dir = sys.stdout.getvalue().strip()
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout
        kernel_path = pathlib.Path(data_dir).joinpath("kernels")
    if not kernel_path.exists():
        kernel_path.mkdir(parents=True, exist_ok=True)
    return kernel_path


def install(kernel_dir=None, kernel_name="blender", overwrite=True):
    """
    Install kernel to jupyter notebook
    """
    blender_exec = bpy.app.binary_path
    # check version
    supported_py_version = (3, 10)
    current_py_version = (sys.version_info.major, sys.version_info.minor)
    if current_py_version != supported_py_version:
        message = """
        Current python interpreter version is not {}.{}!
        blender_notebook will link pip packages installed in this interpreter
        to the blender embedded python interpreter. Mismatch in python version
        might cause problem launching the jupyter kernel. Are you sure to
        continue?
        """.format(*supported_py_version)

    # check input
    blender_path = pathlib.Path(blender_exec)
    if not blender_path.exists():
        raise RuntimeError("Invalid blender executable path!")

    kernel_path = get_kernel_path(kernel_dir)

    kernel_install_path = kernel_path.joinpath(kernel_name)
    if kernel_install_path.exists():
        if not overwrite:
            print(f"kernel '{kernel_name}' already exists, not overwriting.")
            return
        print(f"kernel '{kernel_name}' already exists, overwriting.")
        shutil.rmtree(kernel_install_path)

    # check files to copy
    kernel_py_path = pathlib.Path(__file__).parent.joinpath("kernel.py")
    kernel_launcher_py_path = pathlib.Path(__file__).parent.joinpath(
        "kernel_launcher.py"
    )
    assert kernel_py_path.exists()
    assert kernel_launcher_py_path.exists()

    # create directory
    kernel_install_path.mkdir()

    # copy python files
    kernel_py_dst = kernel_install_path.joinpath(kernel_py_path.name)
    kernel_launcher_py_dst = kernel_install_path.joinpath(kernel_launcher_py_path.name)

    shutil.copyfile(kernel_py_path, kernel_py_dst)
    shutil.copyfile(kernel_launcher_py_path, kernel_launcher_py_dst)
    kernel_launcher_py_dst.chmod(0o755)

    # find python path
    python_path = list()
    for path in sys.path:
        if pathlib.Path(path).is_dir():
            python_path.append(str(path))

    # dump jsons
    kernel_dict = {
        "argv": [
            sys.executable,
            str(kernel_launcher_py_dst),
            "-f",
            r"{connection_file}",
        ],
        "display_name": kernel_name,
        "language": "python",
    }
    blender_config_dict = {
        "blender_executable": str(blender_exec),
        "python_path": str(EXTENSIONS_SITE_PACKAGES),
    }
    kernel_json_dst = kernel_install_path.joinpath("kernel.json")
    blender_config_json_dst = kernel_install_path.joinpath("blender_config.json")
    print(f"{kernel_json_dst=}")
    print(f"{kernel_dict=}")
    with kernel_json_dst.open("w") as f:
        json.dump(kernel_dict, f, indent=2)
    with blender_config_json_dst.open("w") as f:
        json.dump(blender_config_dict, f, indent=2)


def remove(kernel_name, kernel_dir=None):
    """
    Remove the kernel
    """
    kernel_path = get_kernel_path(kernel_dir)
    kernel_install_path = kernel_path.joinpath(kernel_name)
    if not kernel_install_path.exists():
        print(f"Kernal {kernel_name} at {kernel_path} does not exist.")
        return

    shutil.rmtree(kernel_install_path)
    print(f"{kernel_name} jupyter kernel is removed!")
