from setuptools import setup

setup(
    name="WixOS",
    version="2.0.0",
    author="Aras Tokdemir",
    author_email="aras.tokdemir@outlook.com",
    description="WixOS Package",
    packages=["WixOS"],
    install_requires=[
        "Pillow",
        "psutil",
        "PyQt5",
        "psutil",

    ],
    entry_points={
        "console_scripts": [
        "wix-main = WixOS.main:main",
        ],
    },
)
