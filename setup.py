from setuptools import setup
import pathlib
with pathlib.Path(__file__).parent.joinpath('README.md').open('r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "BNotebooks",
    version = "0.0.1",
    description = "A command line tool to wrap blender as a jupyter kernel",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = "Brady Johnston",
    author_email = "brady.johnston@me.com",
    license = "MIT",
    classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
    ],
    packages = ["blender_notebook"],
    zip_safe = True,
    install_requires = [
        'ipykernel',
        'notebook'
    ],
    python_requires = '>=3.10',
    entry_points = {
        'console_scripts': [
            'blender_notebook = blender_notebook.installer:main',
            'blender-notebook = blender_notebook.installer:main'
        ]
    }
)