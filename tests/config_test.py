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

import chws_tool


def test_config_for_font_name():
    config = chws_tool.GoogleFontsConfig.default

    mplus_1p = config.for_font_name("Mplus 1p", False)
    assert mplus_1p is not config
    assert mplus_1p.language == "JAN"

    zhi_mang_xing = config.for_font_name("Zhi Mang Xing", False)
    assert zhi_mang_xing is not config
    assert zhi_mang_xing.language == "ZHS"

    assert config.for_font_name("never exists", False) is None
