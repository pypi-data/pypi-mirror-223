from setuptools import setup, find_packages

setup(
    name="zakirpack",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "zakirpack": ["eCon_36.pyd", "eCon_37.pyd", "eCon_38.pyd", "eCon_39.pyd", "eCon_310.pyd"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
