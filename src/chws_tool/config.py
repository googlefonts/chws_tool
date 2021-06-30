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

import typing

import east_asian_spacing as chws


def _get_factory_by_name() -> typing.Dict[
    str, typing.Callable[[chws.Config, str, bool], typing.Optional[chws.Config]]
]:
    # `not_applicable` disables adding the feature.
    def not_applicable(config, name, is_vertical):
        return None

    # `has_no_pairs` is the same as `not_applicable` but indicates that the tool
    # did not produce any pairs for them, and therefore they are not tested.
    has_no_pairs = not_applicable

    def jan(config, name, is_vertical):
        return config.for_language("JAN")

    def jan_no_vert(config, name, is_vertical):
        if is_vertical:
            return None
        return config.for_language("JAN")

    def jan_mplus1p(config, name, is_vertical):
        config = config.clone()
        config.language = "JAN"
        # These glyphs are wider than half-width and that they collide if
        # kernings are applied.
        config.remove(0x300A, 0x300B)
        if is_vertical:
            config.remove(0x2018, 0x201C)
        return config

    def jan_new_tegomin(config, name, is_vertical):
        config = config.clone()
        config.language = "JAN"
        if is_vertical:
            config.remove(0x2018, 0x201C, 0x3009, 0x300B, 0x300F, 0xFF0C, 0xFF0E)
        return config

    def jan_potta_one(config, name, is_vertical):
        config = config.clone()
        config.language = "JAN"
        if is_vertical:
            config.remove(0x2018, 0x201C)
        return config

    def kor(config, name, is_vertical):
        return config.for_language("KOR")

    def zhs(config, name, is_vertical):
        return config.for_language("ZHS")

    def zhs_middle_colon_semicolon_exclam_question(config, name, is_vertical):
        config = config.clone()
        config.language = "ZHS"
        # These glyphs are supposed to be on the left-half in ZHS fonts,
        # but this font has them at the middle, similar to JAN/ZHT fonts.
        config.is_colon_semicolon_middle = True
        # U+FF01 FULLWIDTH EXCLAMATION MARK
        # U+FF1F FULLWIDTH QUESTION MARK
        config.remove(0xFF01, 0xFF1F)
        return config

    def zhs_long_cang(config, name, is_vertical):
        config = zhs_middle_colon_semicolon_exclam_question(config, name, is_vertical)
        config.remove(0xFF0C, 0xFF0E, 0xFF5B, 0xFF5D)
        return config

    def zhs_ma_shan_zheng(config, name, is_vertical):
        config = zhs_middle_colon_semicolon_exclam_question(config, name, is_vertical)
        config.remove(0xFF08, 0xFF09, 0xFF0C, 0xFF0E, 0xFF3B, 0xFF3D, 0xFF5B, 0xFF5D)
        return config

    def zhs_zcool_qingke_huangyou(config, name, is_vertical):
        config = zhs_middle_colon_semicolon_exclam_question(config, name, is_vertical)
        config.remove(0x300E, 0x3014, 0x3015, 0x3016, 0x3017, 0xFF0C, 0xFF0E)
        return config

    return {
        # JAN
        # "Dela Gothic One" lacks several vertical alternate glyphs.
        "Dela Gothic One": jan_no_vert,
        "DotGothic16": jan,
        "Hachi Maru Pop": jan,
        "Kiwi Maru": jan,
        "Kiwi Maru Light": jan,
        "Kiwi Maru Medium": jan,
        "MotoyaLCedar": jan,
        "MotoyaLMaru": jan,
        "Mplus 1p": jan_mplus1p,
        "Mplus 1p Black": jan_mplus1p,
        "Mplus 1p Bold": jan_mplus1p,
        "Mplus 1p ExtraBold": jan_mplus1p,
        "Mplus 1p Light": jan_mplus1p,
        "Mplus 1p Medium": jan_mplus1p,
        "Mplus 1p Thin": jan_mplus1p,
        "Rounded Mplus 1c": jan_mplus1p,
        "Rounded Mplus 1c Black": jan_mplus1p,
        "Rounded Mplus 1c Bold": jan_mplus1p,
        "Rounded Mplus 1c ExtraBold": jan_mplus1p,
        "Rounded Mplus 1c Light": jan_mplus1p,
        "Rounded Mplus 1c Medium": jan_mplus1p,
        "Rounded Mplus 1c Thin": jan_mplus1p,
        "New Tegomin": jan_new_tegomin,
        "Potta One": jan_potta_one,
        "Reggae One": jan,
        "RocknRoll One": jan,
        "Sawarabi Gothic": jan,
        # "Sawarabi Mincho" has Issues in vertical flow, even without the
        # feature.
        "Sawarabi Mincho": jan_no_vert,
        "Shippori Mincho": jan,
        "Shippori Mincho B1": jan,
        "Shippori Mincho B1 ExtraBold": jan,
        "Shippori Mincho B1 Medium": jan,
        "Shippori Mincho B1 SemiBold": jan,
        "Shippori Mincho ExtraBold": jan,
        "Shippori Mincho Medium": jan,
        "Shippori Mincho SemiBold": jan,
        "Stick": jan,
        "Train One": jan,
        "Yusei Magic": jan,
        # KOR
        "Black And White Picture": has_no_pairs,
        "Black Han Sans": has_no_pairs,
        "Cute Font": has_no_pairs,
        "Do Hyeon": has_no_pairs,
        "Dokdo": has_no_pairs,
        "East Sea Dokdo": has_no_pairs,
        "Gaegu": has_no_pairs,
        "Gaegu Light": has_no_pairs,
        "Gamja Flower": has_no_pairs,
        "Gothic A1": has_no_pairs,
        "Gothic A1 Black": has_no_pairs,
        "Gothic A1 ExtraBold": has_no_pairs,
        "Gothic A1 ExtraLight": has_no_pairs,
        "Gothic A1 Light": has_no_pairs,
        "Gothic A1 Medium": has_no_pairs,
        "Gothic A1 SemiBold": has_no_pairs,
        "Gothic A1 Thin": has_no_pairs,
        "Gugi": has_no_pairs,
        "Hi Melody": has_no_pairs,
        "Jua": has_no_pairs,
        "Kirang Haerang": has_no_pairs,
        # "Nanum Brush Script" has no applicable pairs in horizontal flows, and
        # vertical flow has issues even without the feature.
        "Nanum Brush Script": not_applicable,
        "NanumGothic": kor,
        "NanumGothicExtraBold": kor,
        # Don't apply to "NanumGothicCoding", this is a monospace font.
        "NanumGothicCoding": not_applicable,
        "NanumMyeongjo": has_no_pairs,
        "NanumMyeongjoExtraBold": has_no_pairs,
        # Same as "Nanum Brush Script".
        "Nanum Pen": not_applicable,
        "Poor Story": has_no_pairs,
        "Single Day": has_no_pairs,
        "Song Myung": has_no_pairs,
        "Stylish": has_no_pairs,
        "Sunflower": has_no_pairs,
        "Sunflower Light": has_no_pairs,
        "Sunflower Medium": has_no_pairs,
        "Yeon Sung": has_no_pairs,
        # ZHS
        "Liu Jian Mao Cao": has_no_pairs,
        "Long Cang": zhs_long_cang,
        "Ma Shan Zheng": zhs_ma_shan_zheng,
        "ZCOOL KuaiLe": zhs_middle_colon_semicolon_exclam_question,
        "ZCOOL QingKe HuangYou": zhs_zcool_qingke_huangyou,
        "ZCOOL XiaoWei": zhs_middle_colon_semicolon_exclam_question,
        "Zhi Mang Xing": zhs_middle_colon_semicolon_exclam_question,
    }


class GoogleFontsConfig(chws.NotoCJKConfig):
    _factory_by_name = _get_factory_by_name()

    def for_font_name(
        self, name: str, is_vertical: bool
    ) -> typing.Optional[chws.Config]:
        factory = GoogleFontsConfig._factory_by_name.get(name)
        if factory:
            return factory(self, name, is_vertical)

        # Delegate Noto CJK to `NotoCJKConfig`.
        if name.startswith("Noto "):
            return super().for_font_name(name, is_vertical)

        # Ignore unknown fonts.
        # We prefer manual visual check over relying on heuristic rules.
        return None


GoogleFontsConfig.default = GoogleFontsConfig()
