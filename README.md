[![Continuous Test + Deploy](https://github.com/googlefonts/chws_tool/actions/workflows/ci.yml/badge.svg)](https://github.com/googlefonts/chws_tool/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/chws-tool.svg)](https://pypi.org/project/chws-tool/)
[![Dependencies](https://badgen.net/github/dependabot/googlefonts/chws_tool)](https://github.com/googlefonts/chws_tool/network/updates)

# chws_tool

This tool adds the OpenType
[`chws`], [`vchw`], [`halt`], and [`vhal`]
features to OpenType fonts if any of these features are missing.
Please see [east-asian-sapcing] for details of these features.

This tool uses the [east-asian-sapcing] package as its core engine,
and has following advantages:
* Simpler API and command line options.
* Supports CJK fonts at [fonts.google.com] in its built-in [config].

To add new fonts to the supported font list,
please see the [Adding Fonts] section below.

[east-asian-sapcing]: https://github.com/kojiishi/east_asian_spacing
[`chws`]: https://docs.microsoft.com/en-us/typography/opentype/spec/features_ae#tag-chws
[`halt`]: https://docs.microsoft.com/en-us/typography/opentype/spec/features_fj#tag-halt
[`vchw`]: https://docs.microsoft.com/en-us/typography/opentype/spec/features_uz#tag-vchw
[`vhal`]: https://docs.microsoft.com/en-us/typography/opentype/spec/features_uz#tag-vhal
[fonts.google.com]: https://fonts.google.com/

## Install

```sh
pip install chws-tool
```
If you want to clone and install
in the [editable mode] with the development packages:
```sh
git clone https://github.com/googlefonts/chws_tool.git
cd chws_tool
pip install -e '.[dev]'
```

[editable mode]: https://pip.pypa.io/en/stable/cli/pip_install/#install-editable

## Command Line Usage

The following example adds the features to `input.otf`
and saves it to the `build` directory.
If the argument is a directory,
the tool expands it to all fonts in the directory recursively.
```sh
add-chws input.otf
```
Use the `-o` option to change the output directory,
or the `--help` option for the full list of options.
```sh
add-chws input_dir -o output_dir
```

## API

```python
import chws_tool

def main():
    output_path = chws_tool.add_chws("fonts/input.otf", "build")
    if output_path:
        print("Success!")
    else:
        print("Skipped")
```
For [asyncio] programs:
```python
import asyncio
import chws_tool

async def main_async():
    output_path = await chws_tool.add_chws_async("fonts/input.otf", "build")
    if output_path:
        print("Success!")
    else:
        print("Skipped")

asyncio.run(main_async())
```

[asyncio]: https://docs.python.org/3/library/asyncio.html

## Adding Fonts
[adding fonts]: #adding-fonts

This package has a built-in list of supported fonts in its [config].
The list indicates these fonts passed the [visual test],
with possibly tweaked configurations.

Fonts not in the known list are still processed
with the default configuration,
but this package shows a warning message.

When adding new fonts to the known font list,
the following process is recommended:

1. Find the font names.
   Running the `add-chws` with `--dump-name` option can print them.
2. Add them to the [config].
3. Build the font and run the [Visual Test].
4. Tweak the [config] if needed.

[config]: src/chws_tool/config.py

## Visual Test
[Visual Test]: #visual-test

The primary purpose of this process is to find
too tight spacings or glyph collisions caused by the kernings.

This tool has heuristic rules to determine
the applicability of the spacings using the glyph metrics,
but assumes that full-width punctuation glyphs have enough internal spacings
according to linguistic conventions
as in [UAX#50](http://unicode.org/reports/tr50/#vertical_alternates)
or in [CLREQ](https://w3c.github.io/clreq/#h-punctuation_adjustment_space).
Unfortunately, not all fonts follow the conventions.

To run the visual test:

1. Add the test font to the font list
   in the top `<script>` block of [`tests/test.html`](tests/test.html).
2. Open it in your browser.
3. Check "Fullwidth", "Upright", and "Hide same size" check boxes.

Here is the check list and tips:

* Find where glyphs are too tight or collide
  when the feature is on but look fine without the feature.
  - Quotation marks can collide most often,
    especially in vertical flow but sometimes in horizontal flow too.
  - "Open+Open" and "Close+Close" are more likely to collide than other pairs.
  - Select glyphs to check how much inks overflow the glyph metrics.
* Test both horizontal and vertical flows
  by flipping the "Vertical" checkbox.

Other controls in the test are not mandatory,
but they may be useful in following cases.

* Uncheck "Hide same size" to see cases where kernings are not applied
  by the built-in rules.
  They are usually fine.
  In most cases, they are because the glyphs are missing,
  they are not full-width,
  or the pair should not apply for the script of the font.
  The test file contaisn code poitns for all East Asian scripts,
  but not all code points should apply spacings for all script.
* The "Language" list does not matter in most cases,
  except when the font supports multiple locales,
  such as Noto CJK.
* The "Fullwidth" feature can change glyphs,
  but in most cases,
  if glyphs look ok with the feature on,
  they should be ok with the feature off.
* The "Upright" feature is only valid in the vertical flow.
  You can just check it on,
  for the same reason as the "Fullwidth" feature.
* The "Characters" input fields can change the test cases.
  You don't have to change them unless you have specific needs.
