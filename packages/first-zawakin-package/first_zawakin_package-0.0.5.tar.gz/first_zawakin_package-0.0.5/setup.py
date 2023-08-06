#!/usr/bin/env python
from __future__ import unicode_literals

import os
import io
from setuptools import setup, find_packages


def setup_package():
    package_name = "first_zawakin_package"
    root = os.path.abspath(os.path.dirname(__file__))

    # Read in package meta from about.py
    # about_path = os.path.join(root, package_name, "about.py")
    # with io.open(about_path, encoding="utf8") as f:
    #     about = {}
    #     exec(f.read(), about)

    # Get readme
    readme_path = os.path.join(root, "README.md")
    with io.open(readme_path, encoding="utf8") as f:
        readme = f.read()

    setup(
        name=package_name,
        description='my description',
        long_description=readme,
        long_description_content_type="text/markdown",
        author='zawakin',
        author_email='zawawahoge@gmail.com',
        url='',
        version='0.0.5',
        license='MIT',
        packages=find_packages(),
        keywords=["zawakin"],
        install_requires=[],
        zip_safe=True,
    )


if __name__ == "__main__":
    setup_package()
