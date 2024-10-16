from typing import Optional

from models.character import Character
import models.stats
from util.errors import CharacterException
from util import db

def db_activate_character(user_id: int, character_id: int) -> None:
    cursor = db.conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM active_character WHERE user_id = ?', (user_id))
    number_of_rows = cursor.fetchone()[0]

    if number_of_rows == 0:
        cursor.execute('INSERT INTO active_character (user_id, character_id) VALUES (?, ?)', (user_id, character_id))
    else:
        cursor.execute('UPDATE active_character SET character_id = ? WHERE user_id = ?', (character_id, user_id))
    db.conn.commit()
    cursor.close()

def create_character(user_id: int, name: str) -> Character:
    new_character = Character(name)

    cursor = db.conn.cursor()
    cursor.execute('INSERT INTO character (user_id, name) VALUES (?, ?)', (user_id, name))
    character_id = cursor.lastrowid
    cursor.close()
    db.conn.commit()
    db_activate_character(user_id, character_id)

    return new_character

def activate_character(user_id: int, name: str) -> bool:
    character_list = get_characters_owned_by_user(user_id)
    if character_list is None:
        return False

    match = None
    for character in character_list:
        if character.name == name:
            match = character

    if match is None:
        return False

    db_activate_character(user_id, match.id)
    return True

def find_character_by_name(character_name: str) -> Optional[Character]:
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM character WHERE name = ?', (character_name))

def get_active_character_by_user_id(user_id: int) -> Optional[Character]:
    cursor = db.conn.cursor()
    cursor.execute('SELECT character_id FROM active_character WHERE user_id = ?', (user_id))
    output = cursor.fetchone()
    if output is None:
        return None

    cursor.execute('SELECT * FROM character WHERE id = ?', (output[0]))
    output = cursor.fetchall()
    for row in output:
        print(row)
    cursor.close()
    return Character('Unimplemented')

def get_characters_owned_by_user(user_id: int) -> Optional[list]:
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM character WHERE user_id = ?', (user_id))
    output = cursor.fetchall()
    for row in output:
        print(row)
    cursor.close()
    return list()

def set_skill(user_id: int, skill_name: str, value: int) -> bool:
    character = get_active_character_by_user_id(user_id)
    if character is None:
        raise CharacterException('Character not found.')

    skill = models.stats.get_skill_by_name(skill_name)

    if skill is None:
        raise CharacterException('Invalid skill name.')

    character.set_skill(skill, value)
    return True

def init_db():
    # Create a cursor object using the cursor() method
    cursor = db.conn.cursor()

    # Create tables if we need to
    cursor.execute('''CREATE TABLE IF NOT EXISTS character
                   (id INTEGER PRIMARY KEY, user_id, name, description, image_url, health, morale)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS active_character
        (user_id INTEGER PRIMARY KEY,
        character_id,
        CONSTRAINT fk_character
            FOREIGN KEY (character_id)
            REFERENCES character (id)
            ON DELETE CASCADE
        )''')
    cursor.close()

    # Save (commit) the changes
    db.conn.commit()

init_db()
