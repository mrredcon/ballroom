from models.attribute import Attribute
from models.skill import Skill
from util.errors import CharacterException

class Character:
    def __init__(self, name) -> None:
        self.id = 1
        self.name = name
        self.description = ''
        self._attributes = { x:0 for x in Attribute.__members__ }
        self._skills = { x:0 for x in Skill.__members__ }

    def get_skills_by_attribute(self, attribute: Attribute) -> dict:
        skills_of_attribute = attribute.get_skills()
        return dict((k, self._skills[k]) for k in skills_of_attribute if k in self._skills)

    def get_effective_skill(self, skill: Skill) -> int:
        matching_attribute = skill.get_attribute()
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
