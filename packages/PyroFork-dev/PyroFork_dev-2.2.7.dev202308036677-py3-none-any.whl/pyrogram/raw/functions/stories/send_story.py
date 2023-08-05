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


class SendStory(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``160``
        - ID: ``424CD47A``

    Parameters:
        media (:obj:`InputMedia <pyrogram.raw.base.InputMedia>`):
            N/A

        privacy_rules (List of :obj:`InputPrivacyRule <pyrogram.raw.base.InputPrivacyRule>`):
            N/A

        random_id (``int`` ``64-bit``):
            N/A

        pinned (``bool``, *optional*):
            N/A

        noforwards (``bool``, *optional*):
            N/A

        caption (``str``, *optional*):
            N/A

        entities (List of :obj:`MessageEntity <pyrogram.raw.base.MessageEntity>`, *optional*):
            N/A

        period (``int`` ``32-bit``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyrogram.raw.base.Updates>`
    """

    __slots__: List[str] = ["media", "privacy_rules", "random_id", "pinned", "noforwards", "caption", "entities", "period"]

    ID = 0x424cd47a
    QUALNAME = "functions.stories.SendStory"

    def __init__(self, *, media: "raw.base.InputMedia", privacy_rules: List["raw.base.InputPrivacyRule"], random_id: int, pinned: Optional[bool] = None, noforwards: Optional[bool] = None, caption: Optional[str] = None, entities: Optional[List["raw.base.MessageEntity"]] = None, period: Optional[int] = None) -> None:
        self.media = media  # InputMedia
        self.privacy_rules = privacy_rules  # Vector<InputPrivacyRule>
        self.random_id = random_id  # long
        self.pinned = pinned  # flags.2?true
        self.noforwards = noforwards  # flags.4?true
        self.caption = caption  # flags.0?string
        self.entities = entities  # flags.1?Vector<MessageEntity>
        self.period = period  # flags.3?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendStory":
        
        flags = Int.read(b)
        
        pinned = True if flags & (1 << 2) else False
        noforwards = True if flags & (1 << 4) else False
        media = TLObject.read(b)
        
        caption = String.read(b) if flags & (1 << 0) else None
        entities = TLObject.read(b) if flags & (1 << 1) else []
        
        privacy_rules = TLObject.read(b)
        
        random_id = Long.read(b)
        
        period = Int.read(b) if flags & (1 << 3) else None
        return SendStory(media=media, privacy_rules=privacy_rules, random_id=random_id, pinned=pinned, noforwards=noforwards, caption=caption, entities=entities, period=period)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.pinned else 0
        flags |= (1 << 4) if self.noforwards else 0
        flags |= (1 << 0) if self.caption is not None else 0
        flags |= (1 << 1) if self.entities else 0
        flags |= (1 << 3) if self.period is not None else 0
        b.write(Int(flags))
        
        b.write(self.media.write())
        
        if self.caption is not None:
            b.write(String(self.caption))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        b.write(Vector(self.privacy_rules))
        
        b.write(Long(self.random_id))
        
        if self.period is not None:
            b.write(Int(self.period))
        
        return b.getvalue()
