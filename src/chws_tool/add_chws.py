#!/usr/bin/env python3
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

import argparse
import asyncio
import logging
import os
import pathlib
import time
import typing

import east_asian_spacing as chws
from chws_tool.config import GoogleFontsConfig

logger = logging.getLogger("add_chws")


async def add_chws(
    input: typing.Union[str, os.PathLike],
    output: typing.Union[str, os.PathLike],
) -> typing.Optional[pathlib.Path]:
    """Add OpenType chws/vchw features to a font.

    Returns the path of the output font,
    or `None` if the feature is not applicable to the font."""

    builder = chws.Builder(input, config=GoogleFontsConfig.default)
    await builder.build()
    if not builder.has_spacings:
        if builder.config.for_font(builder.font) is None:
            logger.info('Skipped by config: "%s"', input)
        else:
            logger.warning('Skipped due to no changes: "%s"', input)
        return None

    output_path = builder.save(output)
    logger.info("%s ==> %s", input, output_path)

    await builder.test()

    return output_path


async def main_async() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--dump-name", help="dump font names", action="store_true")
    parser.add_argument(
        "-o", "--output", default="build", type=pathlib.Path, help="output directory"
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="count", default=0
    )
    args = parser.parse_args()
    chws.init_logging(args.verbose, main=logger)

    # Expand directories.
    inputs = chws.Builder.expand_paths(args.inputs)

    if args.dump_name:
        for input in inputs:
            font = chws.Font.load(input)
            fonts = font.fonts_in_collection if font.is_collection else (font,)
            for font in fonts:
                print(font.debug_name(1))
        return

    args.output.mkdir(exist_ok=True, parents=True)
    for input in inputs:
        await add_chws(input, args.output)


def main() -> None:
    start_time = time.time()
    asyncio.run(main_async())
    logger.info(f"Elapsed {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()
