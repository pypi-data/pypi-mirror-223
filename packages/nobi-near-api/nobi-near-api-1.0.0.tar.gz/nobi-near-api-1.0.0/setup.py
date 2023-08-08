from setuptools import setup, find_packages

META_DATA = dict(
    name="nobi-near-api",
    version="1.0.0",
    license="MIT",

    author="NEAR Inc",

    url="https://github.com/parizad1188/near-api-py",

    packages=find_packages(),

    install_requires=["requests", "base58", "ed25519"]
)

if __name__ == "__main__":
    setup(**META_DATA)
