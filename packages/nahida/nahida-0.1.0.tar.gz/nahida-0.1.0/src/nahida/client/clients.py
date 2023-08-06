""""""

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "NSFWCategory",
    "SFWCategory",
    "Configuration",
    "URLs",
    "Image",
    "NSFWResource",
    "SFWResource",
    "Client",
)

import typing

import attrs
import httpx

NSFWCategory = typing.Literal["waifu", "neko", "trap", "blowjob"]
SFWCategory = typing.Literal[
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kill",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe",
]


@attrs.define
class Configuration:
    """"""

    url: httpx.URL


@attrs.define
class URLs:
    """"""

    configuration: Configuration

    def nsfw(self, category: NSFWCategory) -> str:
        """"""
        return self.configuration.url / "nsfw" / category

    def sfw(self, category: SFWCategory) -> str:
        """"""
        return self.configuration.url / "sfw" / category


@attrs.define
class Image:
    """"""

    url: str


@attrs.define
class NSFWResource:
    """"""

    urls: URLs

    def search(self, category: NSFWCategory) -> Image:
        """"""
        url = self.urls.nsfw(category)

        response = httpx.get(url)

        image = Image(**response.json())

        return image


@attrs.define
class SFWResource:
    """"""

    urls: URLs

    def search(self, category: SFWCategory) -> Image:
        """"""
        url = self.urls.sfw(category)

        response = httpx.get(url)

        image = Image(**response.json())

        return image


@attrs.define
class Client:
    """"""

    __url = httpx.URL("https://api.waifu.pics")

    __configuration = Configuration(__url)

    __urls = URLs(__configuration)

    __nsfw_resource = NSFWResource(__urls)
    __sfw_resource = SFWResource(__urls)

    @property
    def nsfw(self) -> NSFWResource:
        """"""
        return self.__nsfw_resource

    @property
    def sfw(self) -> SFWResource:
        """"""
        return self.__sfw_resource


# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
