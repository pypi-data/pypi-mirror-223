#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class SetAccountTTL(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``160``
        - ID: ``2442485E``

    Parameters:
        ttl (:obj:`AccountDaysTTL <pyrogram.raw.base.AccountDaysTTL>`):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["ttl"]

    ID = 0x2442485e
    QUALNAME = "functions.account.SetAccountTTL"

    def __init__(self, *, ttl: "raw.base.AccountDaysTTL") -> None:
        self.ttl = ttl  # AccountDaysTTL

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetAccountTTL":
        # No flags
        
        ttl = TLObject.read(b)
        
        return SetAccountTTL(ttl=ttl)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.ttl.write())
        
        return b.getvalue()
