from typing import Optional

from models.item import Item
import models.stats
from util.errors import CharacterException, ItemException, PermissionException, StatException
from util import db
import services.charactersvc

def create_item(user_id: int, name: str) -> Item:
    cursor = db.conn.cursor()
    cursor.execute('INSERT INTO item (user_id, name) VALUES (?, ?)', (user_id, name,))
    item_id = cursor.lastrowid
    cursor.close()
    db.conn.commit()
    return Item(item_id, user_id, name, None, None, None, None, None)

def find_item_by_name(item_name: str) -> Optional[Item]:
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM item WHERE name = ?', (item_name,))
    db_item = cursor.fetchone()
    return Item(*db_item)

def get_items_owned_by_user(user_id: int) -> Optional[list[Item]]:
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM item WHERE user_id = ?', (user_id,))
    output = cursor.fetchall()
    items = list()
    for row in output:
        items.append(Item(*row))
    cursor.close()
    return items

def get_character_inventory(user_id: int) -> Optional[dict[Item, int]]:
    character = services.charactersvc.get_active_character_by_user_id(user_id)
    if character is None:
        raise CharacterException('Character not found.')
    character_id = character.db_id
    cursor = db.conn.cursor()
    cursor.execute('SELECT item_id, quantity FROM inventory WHERE character_id = ?', (character_id,))
    db_inventory = cursor.fetchall()

    inventory = dict()
    for inventory_row in db_inventory:
        cursor.execute('SELECT * FROM item WHERE id = ?', (inventory_row[0],))
        db_item = cursor.fetchone()
        item = Item(*db_item)
        inventory[item] = inventory_row[1]

    cursor.close()
    return inventory

def set_attribute(user_id: int, item_name: str, attribute_name: str, value: int) -> None:
    item = find_item_by_name(item_name)
    if item is None:
        raise ItemException('Item not found.')

    if user_id != item.user_id:
        raise PermissionException('Only the owner of the item may edit its statistics.')

    attribute = models.stats.get_attribute_by_name(attribute_name)

    if attribute is None:
        raise StatException('Invalid attribute name.')

    cursor = db.conn.cursor()
    cursor.execute(('INSERT INTO item_stat(item_id, stat_name, value) '
                    'VALUES (?, ?, ?) ON CONFLICT (item_id, stat_name) DO UPDATE SET value=?'),
                    (item.db_id, attribute.name, value, value))
    cursor.close()
    db.conn.commit()

def set_skill(user_id: int, item_name: str, skill_name: str, value: int) -> None:
    item = find_item_by_name(item_name)
    if item is None:
        raise ItemException('Item not found.')

    if user_id != item.user_id:
        raise PermissionException('Only the owner of the item may edit its statistics.')

    skill = models.stats.get_skill_by_name(skill_name)

    if skill is None:
        raise StatException('Invalid skill name.')

    cursor = db.conn.cursor()
    cursor.execute(('INSERT INTO item_stat(item_id, stat_name, value) '
                    'VALUES (?, ?, ?) ON CONFLICT (item_id, stat_name) DO UPDATE SET value=?'),
                    (item.db_id, skill.name, value, value))
    cursor.close()
    db.conn.commit()

def init_db():
    # Create a cursor object using the cursor() method
    cursor = db.conn.cursor()

    # Create tables if we need to
    cursor.execute('''CREATE TABLE IF NOT EXISTS item
                   (id INTEGER PRIMARY KEY, user_id, name, description, image_url, slot, item_type, duration)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS item_stat
        (item_id,
        stat_name,
        stat_desc,
        value,
        PRIMARY KEY (item_id, stat_name)
        CONSTRAINT fk_item
            FOREIGN KEY (item_id)
            REFERENCES item (id)
            ON DELETE CASCADE
        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory
        (character_id,
        item_id,
        quantity,
        equipped,
        PRIMARY KEY (character_id, item_id)
        CONSTRAINT fk_character
            FOREIGN KEY (character_id)
            REFERENCES character (id)
            ON DELETE CASCADE
        CONSTRAINT fk_item
            FOREIGN KEY (item_id)
            REFERENCES item (id)
            ON DELETE CASCADE
        )''')

    cursor.close()

    # Save (commit) the changes
    db.conn.commit()

init_db()
