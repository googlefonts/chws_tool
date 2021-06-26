# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages


setup_args = dict(
    name="chws_tool",
    use_scm_version={"write_to": "src/chws_tool/_version.py"},
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'add-chws=chws_tool.add_chws:main',
        ],
    },
    setup_requires=["setuptools_scm"],
    install_requires=[
        "east-asian-spacing>=1.1.1",
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
            "pytest-asyncio",
            "pytype",
            "tox",
        ],
    },
    python_requires=">=3.8",

    # this is for type checker to use our inline type hints:
    # https://www.python.org/dev/peps/pep-0561/#id18
    package_data={"chws_tool": ["py.typed"]},

    # metadata to display on PyPI
    author="Koji Ishii",
    author_email="kojii@chromium.org",
    description=(
        "Utility for OpenType chws/vchw features"
    ),
)


if __name__ == "__main__":
    setup(**setup_args)
