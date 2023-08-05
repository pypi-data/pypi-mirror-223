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


class GetPinnedStories(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``160``
        - ID: ``B471137``

    Parameters:
        user_id (:obj:`InputUser <pyrogram.raw.base.InputUser>`):
            N/A

        offset_id (``int`` ``32-bit``):
            N/A

        limit (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`stories.Stories <pyrogram.raw.base.stories.Stories>`
    """

    __slots__: List[str] = ["user_id", "offset_id", "limit"]

    ID = 0xb471137
    QUALNAME = "functions.stories.GetPinnedStories"

    def __init__(self, *, user_id: "raw.base.InputUser", offset_id: int, limit: int) -> None:
        self.user_id = user_id  # InputUser
        self.offset_id = offset_id  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetPinnedStories":
        # No flags
        
        user_id = TLObject.read(b)
        
        offset_id = Int.read(b)
        
        limit = Int.read(b)
        
        return GetPinnedStories(user_id=user_id, offset_id=offset_id, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
