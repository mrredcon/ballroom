from dataclasses import dataclass, field
from typing import Optional

from models.item_type import ItemType
from models.itemstat import ItemStat
from models.slot import Slot

@dataclass
class Item:
    db_id: int
    user_id: int
    name: str
    description: str
    image_url: str
    slot: Slot
    item_type: ItemType
    duration: int
    effects: list[ItemStat] = field(default_factory=list)

def construct_item(db_item) -> Optional[Item]:
    if db_item is None:
        return None

    # Convert from Tuple into list so we can mess with it
    db_item = list(db_item)

    if db_item[5] is not None:
        db_item[5] = Slot[db_item[5]]

    if db_item[6] is not None:
        db_item[6] = ItemType[db_item[6]]

    return Item(*db_item)
