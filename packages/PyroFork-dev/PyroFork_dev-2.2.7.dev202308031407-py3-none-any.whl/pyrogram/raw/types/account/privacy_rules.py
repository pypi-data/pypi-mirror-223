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


class PrivacyRules(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.account.PrivacyRules`.

    Details:
        - Layer: ``160``
        - ID: ``50A04E45``

    Parameters:
        rules (List of :obj:`PrivacyRule <pyrogram.raw.base.PrivacyRule>`):
            N/A

        chats (List of :obj:`Chat <pyrogram.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <pyrogram.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetPrivacy
            account.SetPrivacy
    """

    __slots__: List[str] = ["rules", "chats", "users"]

    ID = 0x50a04e45
    QUALNAME = "types.account.PrivacyRules"

    def __init__(self, *, rules: List["raw.base.PrivacyRule"], chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.rules = rules  # Vector<PrivacyRule>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PrivacyRules":
        # No flags
        
        rules = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return PrivacyRules(rules=rules, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.rules))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
