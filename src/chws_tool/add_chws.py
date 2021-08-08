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
import sys
import time
from typing import Optional
from typing import Union

import east_asian_spacing as chws
from chws_tool.config import GoogleFontsConfig

logger = logging.getLogger("add_chws")


async def add_chws_async(
    input: Union[str, os.PathLike],
    output: Optional[Union[str, os.PathLike]] = None,
    **kwargs,
) -> Optional[pathlib.Path]:
    """Add OpenType chws/vchw features to a font.

    Returns the path of the output font,
    or `None` if the feature is not applicable to the font.

    `**kwargs` are optional. They are passed directly to
    `east_asian_spacing.Builder.save()`."""

    builder = chws.Builder(input, config=GoogleFontsConfig.default)
    output_path = await builder.build_and_save(output, **kwargs)
    if not output_path:
        logger.info('Skipped saving due to no changes: "%s"', input)
        return None
    logger.info("%s ==> %s", input, output_path)

    await builder.test()

    return output_path


def add_chws(
    input: Union[str, os.PathLike],
    output: Optional[Union[str, os.PathLike]] = None,
    **kwargs,
) -> Optional[pathlib.Path]:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(add_chws_async(input, output, **kwargs))


def _dump_font_names(inputs):
    for input in inputs:
        font = chws.Font.load(input)
        fonts = font.fonts_in_collection if font.is_collection else (font,)
        for font in fonts:
            print(font.debug_name(1))


async def main_async() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--dump-name", help="dump font names", action="store_true")
    parser.add_argument("-g", "--glyph-out", help="output glyph list")
    parser.add_argument(
        "-o", "--output", default="build", type=pathlib.Path, help="output directory"
    )
    parser.add_argument(
        "-p",
        "--print-path",
        action="store_true",
        help="print the file paths to stdout",
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="count", default=0
    )
    args = parser.parse_args()
    chws.init_logging(args.verbose, main=logger)

    # Expand directories.
    inputs = chws.Builder.expand_paths(args.inputs)

    if args.dump_name:
        _dump_font_names(inputs)
        return

    if args.glyph_out:
        if args.glyph_out == "-":
            args.glyph_out = sys.stdout
        else:
            args.glyph_out = pathlib.Path(args.glyph_out)
            args.glyph_out.mkdir(exist_ok=True, parents=True)
    args.output.mkdir(exist_ok=True, parents=True)

    for input in inputs:
        await add_chws_async(
            input, args.output, glyph_out=args.glyph_out, print_path=args.print_path
        )


def main() -> None:
    start_time = time.time()
    asyncio.run(main_async())
    logger.info(f"Elapsed {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()
