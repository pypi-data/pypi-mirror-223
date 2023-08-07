import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algodojo",
    version="0.2.2",
    author="AlgoDojo team",
    author_email="slin@dojotechs.com",
    description="A automatic trading application of package",
    keywords='quant quantitative investment trading algotrading',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DojoTechs/",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["ibapi",
                      "python-socketio",
                      "requests",
                      "websocket-client",
                      "pandas",
                      "quantstats",
                      "matplotlib"
                      ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)
