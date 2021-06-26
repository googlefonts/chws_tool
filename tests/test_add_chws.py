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

import pytest

import chws_tool
import east_asian_spacing as chws


@pytest.mark.asyncio
async def test_add_chws(noto_sans_cjkjp_otf, tmp_path):
    output_path = await chws_tool.add_chws(noto_sans_cjkjp_otf, tmp_path)
    assert output_path
    assert output_path.exists()

    output_font = chws.Font.load(output_path)
    assert output_font.has_gpos_feature("chws")
    assert output_font.has_gpos_feature("vchw")
