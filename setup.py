from setuptools import setup, find_packages

setup(
    name="nusanxspace",
    version="3.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "colorama"
    ],
    author="Anonys",
    description="Bug Bounty Toolkit",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
