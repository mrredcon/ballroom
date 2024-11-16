from dataclasses import dataclass
from typing import Optional

from models.attribute import Attribute
from models.skill import Skill
from util.errors import StatException

@dataclass
class ItemStat:
    item_id: int
    stat: any
    stat_desc: str
    value: int

def construct_itemstat(db_row) -> Optional[ItemStat]:
    if db_row is None:
        return None

    # Convert from Tuple into list so we can mess with it
    db_row = list(db_row)

    # stat_name can be either an Attribute or Skill
    try:
        db_row[1] = Attribute[db_row[1]]
    except KeyError:
        pass

    try:
        db_row[1] = Skill[db_row[1]]
    except KeyError:
        pass

    if db_row[1] is None:
        raise StatException('stat_name was not a valid Attribute or Skill')

    return ItemStat(*db_row)
