#!/usr/bin/env python3
import async_challonge

from distutils.core import setup

setup(
    name="async-challonge",
    author="ZeLarpMaster",
    url="https://github.com/ZeLarpMaster/async-challonge",
    version=async_challonge.__version__,
    packages=["async_challonge"],
    install_requires=["aiohttp>=3.0.0"]
)
