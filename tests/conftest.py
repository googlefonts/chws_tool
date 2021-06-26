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

import os
import urllib.request

import pytest


@pytest.fixture(scope="session")
def noto_sans_cjkjp_otf(tmp_path_factory):
    """Download "NotoSansCJKjp-Regular.otf"."""
    url_path = "Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf"
    url = "https://raw.githubusercontent.com/googlefonts/noto-cjk/main/"
    url += url_path
    tmp_dir = tmp_path_factory.getbasetemp()
    path = tmp_dir / os.path.basename(url_path)
    with urllib.request.urlopen(url) as response:
        path.write_bytes(response.read())
    return path
