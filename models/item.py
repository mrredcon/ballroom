from models.attribute import Attribute
from models.skill import Skill
from models import stats
from util.errors import CharacterException

class Item:
    def __init__(self, db_id, user_id, name, description, image_url, slot, item_type, duration) -> None:
        # cursor.execute('''CREATE TABLE IF NOT EXISTS item
        #            (id INTEGER PRIMARY KEY, user_id, name, description, image_url, slot, type, duration)''')
        self.db_id = db_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.image_url = image_url
        self.slot = slot
        self.item_type = item_type
        self.duration = duration
        self._attributes = { x:0 for x in Attribute.__members__.values() }
        self._skills = { x:0 for x in Skill.__members__.values() }

    def get_skills_by_attribute(self, attribute: Attribute) -> dict:
        skills_of_attribute = stats.get_skills(attribute)
        return dict((k, self._skills[k]) for k in skills_of_attribute if k in self._skills)

    def get_attribute(self, attribute: Attribute) -> int:
        return self._attributes[attribute]

    def get_effective_skill(self, skill: Skill) -> int:
        matching_attribute = stats.get_attribute(skill)
        attribute_value = self._attributes[matching_attribute]
        return attribute_value + self._skills[skill]

    def set_attribute(self, attribute: Attribute, value: int) -> None:
        if value < 0:
            raise CharacterException('Attribute value cannot be less than 0.')
        self._attributes[attribute] = value

    def set_skill(self, skill: Skill, value: int) -> None:
        if value < 0:
            raise CharacterException('Skill value cannot be less than 0.')
        self._skills[skill] = value
