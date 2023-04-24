from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    readme_description = f.read()


def read_requirements(filename):
    with open(filename, "r", encoding="utf-8") as fp:
        return fp.read().strip().splitlines()


setup(
    name="cain",
    packages=["cain"],
    version="1.0",
    license="MIT License",
    description="A small yet powerful data format!",
    author="Anime no Sekai",
    author_email="niichannomail@gmail.com",
    url="https://github.com/Animenosekai/cain",
    # download_url="https://github.com/Animenosekai/cain/archive/v1.0.tar.gz",
    keywords=[
        "python",
        "cain",
        "data",
        "format"
    ],
    install_requires=read_requirements("requirements.txt"),
    # extras_require={"server": read_requirements("requirements-server.txt"), "dev": read_requirements("requirements-dev.txt")},
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    long_description=readme_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.8, <4",
    # entry_points={"console_scripts": ["cain = cain.__main__:main"]},
    package_data={
        "cain": ["LICENSE"],
    },
)
