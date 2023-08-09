"""
Override Pydantic's BaseModel class to ensure hashable model objects
"""
from pydantic import BaseConfig, BaseModel, Extra


class CycloneDXBaseModel(BaseModel):
    """
    Hoppr CycloneDX base data model
    """

    class Config(BaseConfig):
        """
        Config options for CycloneDXBaseModel
        """

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = Extra.allow
        use_enum_values = True

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        """
        Define to test equality or uniqueness between objects
        """
        return hash(repr(self))
