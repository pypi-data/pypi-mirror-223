import re
from setuptools import find_packages, setup


with open("taku/__init__.py", "r") as fh:
    taku_version = re.findall(r'__version__ = \'(.*?)\'', fh.read())[0]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='taku',
    version=taku_version,
    author='Jiahui Huang',
    author_email='huangjh.work@outlook.com',
    description='Taku: Task managing made easy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://taku.readthedocs.io/en/latest/",
    packages=find_packages(),
    classifiers=[
        "Operating System :: Unix",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords=['task', 'manager'],
    python_requires='>=3.6',
    install_requires=[
        "logging",
        "omegaconf",
        "rich",
    ],
    include_package_data=True,
)
