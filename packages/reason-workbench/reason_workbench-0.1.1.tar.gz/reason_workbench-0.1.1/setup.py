# setup.py
from setuptools import setup, find_packages

setup(
    name="reason_workbench",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "reason_workbench=reason_workbench.main:main",
        ],
    },
    install_requires=[
        "transformers",
        "bert-score",
        "pandas",
        "matplotlib",
    ],
)

