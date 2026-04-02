from setuptools import setup, find_packages

setup(
    name="multicode",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich",
        "prompt-toolkit",
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "multicode = multicode.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={"multicode": ["statuses.txt"]},
    author="cry-nix",
    description="Terminal AI coding assistant",
    license="Apache 2.0",
)
