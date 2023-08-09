#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram import raw
from ..object import Object


class InputReplyToMessage(Object):
    """Contains information about a target replied message.


    Parameters:
        reply_to_message_id (``int``):
            ID of the original message you want to reply.

        message_thread_id (``int``, *optional*):
            Unique identifier for the target message thread (topic) of the forum.
            for forum supergroups only.
    """

    def __init__(
        self, *,
        reply_to_message_id: int,
        message_thread_id: int = None
    ):
        super().__init__()

        if message_thread_id:
            if not reply_to_message_id:
                self.reply_to_msg_id = message_thread_id
            else:
                self.reply_to_msg_id = reply_to_message_id
            self.top_msg_id = message_thread_id
        else:
            self.reply_to_msg_id = reply_to_message_id
