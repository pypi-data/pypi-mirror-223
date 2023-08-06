import sqlite3
import os.path
from dataclasses import dataclass
from glob import glob
from typing import List

from wechat_backup.context import WechatPlatform, WechatContext
from wechat_backup.helper import sqlite_connect


@dataclass
class WechatContextIos(WechatContext):
    doc_dir: str
    contact_db: sqlite3.Connection
    mm_db: sqlite3.Connection
    message_db: List[sqlite3.Connection]


def new_context(profile: dict):
    return WechatContextIos(
        platform=WechatPlatform.iOS,
        user_id=profile['user_id'],
        doc_dir=profile['doc_dir'],
        message_db=[sqlite_connect(db_file) for db_file in glob(f'{os.path.join(profile["doc_dir"], "DB")}/message_*.sqlite')],
        mm_db=sqlite_connect(os.path.join(profile['doc_dir'], 'DB', 'MM.sqlite')),
        contact_db=sqlite_connect(os.path.join(profile['doc_dir'], 'DB', 'WCDB_Contact.sqlite')),
        emoji_cache=profile['emoji_cache']
    )
