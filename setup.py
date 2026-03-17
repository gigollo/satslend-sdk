from setuptools import setup

setup(
    name="satslend",
    version="1.0.0",
    description="Bitcoin-collateralized M2M lending SDK for AI agents and trading bots",
    long_description=open("README.md").read(),
    author="SATS.LEND",
    url="https://satslend.services",
    py_modules=["satslend"],
    install_requires=["requests"],
    python_requires=">=3.7",
    keywords=["bitcoin", "lending", "api", "bot", "ai", "usdc", "defi"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business :: Financial",
    ],
)
