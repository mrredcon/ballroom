from typing import Optional

from models.skill import Skill
from models.attribute import Attribute
from util.errors import StatException

def get_attribute_by_name(query: str) -> Optional[Attribute]:
    match = None

    for name, attribute in Attribute.__members__.items():
        if name.casefold() == query.casefold():
            match = attribute
    return match

_attribute_to_skills = {
    Attribute.INTELLECT: [ Skill.LOGIC, Skill.ENCYCLOPEDIA, Skill.RHETORIC, Skill.DRAMA, Skill.CONCEPTUALIZATION, Skill.VISUALCALCULUS ],
    Attribute.PSYCHE: [ Skill.VOLITION, Skill.INLANDEMPIRE, Skill.EMPATHY, Skill.AUTHORITY, Skill.ESPRITDECORPS, Skill.SUGGESTION ],
    Attribute.PHYSIQUE: [ Skill.ENDURANCE, Skill.PAINTHRESHOLD, Skill.PHYSICALINSTRUMENT, Skill.ELECTROCHEMISTRY, Skill.SHIVERS, Skill.HALFLIGHT ],
    Attribute.MOTORICS: [ Skill.HANDEYECOORDINATION, Skill.PERCEPTION, Skill.REACTIONSPEED, Skill.SAVOIRFAIRE, Skill.INTERFACING, Skill.COMPOSURE ]
}

def get_skills(attribute: Attribute):
    return _attribute_to_skills[attribute]

_skills_to_attribute = {
    Skill.LOGIC: Attribute.INTELLECT,
    Skill.ENCYCLOPEDIA: Attribute.INTELLECT,
    Skill.RHETORIC: Attribute.INTELLECT,
    Skill.DRAMA: Attribute.INTELLECT,
    Skill.CONCEPTUALIZATION: Attribute.INTELLECT,
    Skill.VISUALCALCULUS: Attribute.INTELLECT,

    Skill.VOLITION: Attribute.PSYCHE,
    Skill.INLANDEMPIRE: Attribute.PSYCHE,
    Skill.EMPATHY: Attribute.PSYCHE,
    Skill.AUTHORITY: Attribute.PSYCHE,
    Skill.ESPRITDECORPS: Attribute.PSYCHE,
    Skill.SUGGESTION: Attribute.PSYCHE,

    Skill.ENDURANCE: Attribute.PHYSIQUE,
    Skill.PAINTHRESHOLD: Attribute.PHYSIQUE,
    Skill.PHYSICALINSTRUMENT: Attribute.PHYSIQUE,
    Skill.ELECTROCHEMISTRY: Attribute.PHYSIQUE,
    Skill.SHIVERS: Attribute.PHYSIQUE,
    Skill.HALFLIGHT: Attribute.PHYSIQUE,

    Skill.HANDEYECOORDINATION: Attribute.MOTORICS,
    Skill.PERCEPTION: Attribute.MOTORICS,
    Skill.REACTIONSPEED: Attribute.MOTORICS,
    Skill.SAVOIRFAIRE: Attribute.MOTORICS,
    Skill.INTERFACING: Attribute.MOTORICS,
    Skill.COMPOSURE: Attribute.MOTORICS
}

def get_attribute(skill: Skill):
    return _skills_to_attribute[skill]

_attribute_pretty_names = {
    Attribute.INTELLECT: "Intellect",
    Attribute.PSYCHE: "Psyche",
    Attribute.PHYSIQUE: "Physique",
    Attribute.MOTORICS: "Motorics"
}

_skill_pretty_names = {
    Skill.LOGIC: "Logic",
    Skill.ENCYCLOPEDIA: "Encyclopedia",
    Skill.RHETORIC: "Rhetoric",
    Skill.DRAMA: "Drama",
    Skill.CONCEPTUALIZATION: "Conceptualization",
    Skill.VISUALCALCULUS: "Visual Calculus",

    Skill.VOLITION: "Volition",
    Skill.INLANDEMPIRE: "Inland Empire",
    Skill.EMPATHY: "Empathy",
    Skill.AUTHORITY: "Authority",
    Skill.ESPRITDECORPS: "Esprit de Corps",
    Skill.SUGGESTION: "Suggestion",

    Skill.ENDURANCE: "Endurance",
    Skill.PAINTHRESHOLD: "Pain Threshold",
    Skill.PHYSICALINSTRUMENT: "Physical Instrument",
    Skill.ELECTROCHEMISTRY: "Electrochemistry",
    Skill.SHIVERS: "Shivers",
    Skill.HALFLIGHT: "Half Light",

    Skill.HANDEYECOORDINATION: "Hand/Eye Coordination",
    Skill.PERCEPTION: "Perception",
    Skill.REACTIONSPEED: "Reaction Speed",
    Skill.SAVOIRFAIRE: "Savoir Faire",
    Skill.INTERFACING: "Interfacing",
    Skill.COMPOSURE: "Composure"
}

def get_pretty_name(skill_or_attribute) -> str:
    if skill_or_attribute is Attribute:
        return _attribute_pretty_names[skill_or_attribute]
    if skill_or_attribute is Skill:
        return _skill_pretty_names[skill_or_attribute]
    raise StatException('Given parameter was not an Attribute or Skill.')

_skill_aliases = {
    "encyc": Skill.ENCYCLOPEDIA,
    "ency": Skill.ENCYCLOPEDIA,

    "concept": Skill.CONCEPTUALIZATION,

    "visual": Skill.VISUALCALCULUS,
    "calculus": Skill.VISUALCALCULUS,
    "calc": Skill.VISUALCALCULUS,

    "inland": Skill.INLANDEMPIRE,
    "empire": Skill.INLANDEMPIRE,

    "empath": Skill.EMPATHY,

    "auth": Skill.AUTHORITY,

    "esprit": Skill.ESPRITDECORPS,
    "corps": Skill.ESPRITDECORPS,

    "suggest": Skill.SUGGESTION,

    "endure": Skill.ENDURANCE,

    "pain": Skill.PAINTHRESHOLD,
    "threshold": Skill.PAINTHRESHOLD,

    "physical": Skill.PHYSICALINSTRUMENT,
    "instrument": Skill.PHYSICALINSTRUMENT,

    "electro": Skill.ELECTROCHEMISTRY,
    "chemistry": Skill.ELECTROCHEMISTRY,
    "chem": Skill.ELECTROCHEMISTRY,

    "shiver": Skill.SHIVERS,

    "half": Skill.HALFLIGHT,
    "light": Skill.HALFLIGHT,

    "coord": Skill.HANDEYECOORDINATION,
    "coordination": Skill.HANDEYECOORDINATION,
    "hand": Skill.HANDEYECOORDINATION,
    "handeye": Skill.HANDEYECOORDINATION,

    "percept": Skill.PERCEPTION,
    "perceive": Skill.PERCEPTION,
    "per": Skill.PERCEPTION,

    "react": Skill.REACTIONSPEED,
    "reaction": Skill.REACTIONSPEED,
    "speed": Skill.REACTIONSPEED,

    "savoir": Skill.SAVOIRFAIRE,
    "faire": Skill.SAVOIRFAIRE,

    "interface": Skill.INTERFACING,
    "inter": Skill.INTERFACING,

    "compose": Skill.COMPOSURE
}

def get_skill_by_name(query: str) -> Optional[Skill]:
    match = None

    # check aliases first
    for alias, skill in _skill_aliases.items():
        if alias.casefold() == query.casefold():
            return skill

    for name, skill in Skill.__members__.items():
        if name.casefold() == query.casefold():
            match = skill
    return match
