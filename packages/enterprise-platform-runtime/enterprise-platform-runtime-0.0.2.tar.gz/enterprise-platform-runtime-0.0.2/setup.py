import setuptools

setuptools.setup(
    name="enterprise-platform-runtime",
    version="0.0.2",
    packages=[
        "runtime",
    ],
    install_requires=[
        "cloudpickle",
        "httpx",
        "pydantic==1.10.10",
    ],
)
