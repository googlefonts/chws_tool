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

import logging
import typing

import east_asian_spacing as chws

logger = logging.getLogger("config")


def _get_factory_by_name() -> (
    typing.Dict[
        str, typing.Callable[[chws.Config, str, bool], typing.Optional[chws.Config]]
    ]
):
    def default(config, name, is_vertical):
        return config

    def allow_monospace_ascii(config, name, is_vertical):
        return config.with_skip_monospace_ascii(False)

    def allow_monospace_ascii_no_vert(config, name, is_vertical):
        if is_vertical:
            return None
        return config.with_skip_monospace_ascii(False)

    def use_upem(config, name, is_vertical):
        return config.with_fullwidth_advance(None)

    def use_upem_no_vert(config, name, is_vertical):
        if is_vertical:
            return None
        return config.with_fullwidth_advance(None)

    # `has_no_pairs` indicates that the tool did not produce any pairs for them,
    # and therefore they are not tested.
    def has_no_pairs(config, name, is_vertical):
        return None

    def has_no_vert_pairs(config, name, is_vertical):
        if is_vertical:
            return None
        return config

    # `not_applicable` disables adding the feature.
    def not_applicable(config, name, is_vertical):
        return None

    def _ZCOOL_XiaoWei(config, name, is_vertical):
        # '「」' are not fullwidth.
        return config.with_fullwidth_advance("四水城（）")

    return {
        # JAN
        "Dela Gothic One": use_upem_no_vert,
        "DotGothic16": allow_monospace_ascii,
        "Hachi Maru Pop": default,
        "Hina Mincho": has_no_vert_pairs,
        "Kaisei Decol": default,
        "Kaisei HarunoUmi": default,
        "Kaisei Opti": default,
        "Kaisei Tokumin": default,
        "Kiwi Maru": default,
        "Klee One": default,
        "Kosugi": default,
        "Kosugi Maru": default,
        "Mochiy Pop One": default,
        "Mochiy Pop P One": default,
        "MotoyaLCedar": allow_monospace_ascii,
        "MotoyaLMaru": allow_monospace_ascii,
        "M PLUS 1": default,
        "M PLUS 1 Code": default,
        "M PLUS 2": default,
        "Mplus 1p": default,
        "Mplus 1p Bold": default,
        "Murecho": default,
        "Otomanopee One": has_no_pairs,
        "Rock 3D": default,
        "Rounded Mplus 1c": default,
        "Rounded Mplus 1c Bold": default,
        "New Tegomin": default,
        "Palette Mosaic": not_applicable,
        "Potta One": default,
        "Rampart One": default,
        "Reggae One": default,
        "RocknRoll One": default,
        "Sawarabi Gothic": default,
        "Sawarabi Mincho": default,
        "Shippori Antique": default,
        "Shippori Antique B1": default,
        "Shippori Mincho": default,
        "Shippori Mincho B1": default,
        "Shizuru": default,
        "Stick": default,
        "Train One": default,
        "Yomogi": allow_monospace_ascii_no_vert,
        "Yuji Boku": default,
        "Yuji Hentaigana Akari": default,
        "Yuji Hentaigana Akebono": default,
        "Yuji Mai": default,
        "Yuji Syuku": default,
        "Yusei Magic": has_no_vert_pairs,
        "Zen Antique": default,
        "Zen Antique Soft": default,
        "Zen Kaku Gothic Antique": default,
        "Zen Kaku Gothic New": default,
        "Zen Kurenaido": default,
        "Zen Maru Gothic": default,
        "Zen Old Mincho": default,
        # KOR
        "Black And White Picture": has_no_pairs,
        "Black Han Sans": has_no_pairs,
        "Cute Font": has_no_pairs,
        "Do Hyeon": has_no_pairs,
        "Dokdo": has_no_pairs,
        "East Sea Dokdo": has_no_pairs,
        "Gaegu": has_no_pairs,
        "Gamja Flower": has_no_pairs,
        "Gothic A1": has_no_pairs,
        "Gowun Batang": has_no_pairs,
        "Gowun Dodum": has_no_pairs,
        "Gugi": has_no_pairs,
        "Hahmlet": has_no_pairs,
        "Hi Melody": has_no_pairs,
        "IBM Plex Sans KR": default,
        "Jua": has_no_pairs,
        "Kirang Haerang": has_no_pairs,
        "Nanum Brush Script": not_applicable,
        "NanumGothic": not_applicable,
        "NanumGothicCoding": has_no_pairs,
        "NanumMyeongjo": has_no_pairs,
        "Nanum Pen": not_applicable,
        "Poor Story": has_no_pairs,
        "Single Day": has_no_pairs,
        "Song Myung": has_no_pairs,
        "Stylish": has_no_pairs,
        "Sunflower": has_no_pairs,
        "Yeon Sung": has_no_pairs,
        # ZHS
        "Liu Jian Mao Cao": has_no_pairs,
        "Long Cang": default,
        "Ma Shan Zheng": default,
        "ZCOOL KuaiLe": default,
        "ZCOOL QingKe HuangYou": default,
        "ZCOOL XiaoWei": _ZCOOL_XiaoWei,
        "Zhi Mang Xing": has_no_pairs,
    }


class GoogleFontsConfig(chws.Config):
    _factory_by_name = _get_factory_by_name()

    def for_font_name(
        self, name: str, is_vertical: bool
    ) -> typing.Optional[chws.Config]:
        factory = GoogleFontsConfig._factory_by_name.get(name)
        if factory:
            return factory(self, name, is_vertical)

        # Delegate Noto CJK to `Config`.
        if name.startswith("Noto "):
            return super().for_font_name(name, is_vertical)

        # Ignore unknown fonts.
        # We prefer manual visual check over relying on heuristic rules.
        logger.warning('Not a known font, using the default config: "%s"', name)
        return self


GoogleFontsConfig.default = GoogleFontsConfig()
