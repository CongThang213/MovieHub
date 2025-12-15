from typing import List

from src.domain.models.cast import Cast
from src.infrastructure.database.models.cast_entity import CastEntity


class CastEntityMappers:
    @staticmethod
    def to_domain(entity: CastEntity) -> Cast:
        """Convert a CastEntity to a Cast domain model.

        Args:
            entity (CastEntity): The CastEntity instance to convert.

        Returns:
            Cast: The corresponding Cast domain model.
        """
        return Cast(
            id=entity.id,
            name=entity.name,
            date_of_birth=entity.date_of_birth,
            biography=entity.biography,
        )

    @staticmethod
    def to_domains(entities: List[CastEntity]) -> List[Cast]:
        """Convert a list of CastEntity instances to a list of Cast domain models.

        Args:
            entities (List[CastEntity]): The list of CastEntity instances to convert.

        Returns:
            List[Cast]: The corresponding list of Cast domain models.
        """
        return [CastEntityMappers.to_domain(entity) for entity in entities]

    @staticmethod
    def from_domain(domain: Cast) -> CastEntity:
        """Convert a Cast domain model to a CastEntity.

        Args:
            domain (Cast): The Cast domain model to convert.

        Returns:
            CastEntity: The corresponding CastEntity instance.
        """
        return CastEntity(
            id=domain.id,
            name=domain.name,
            date_of_birth=domain.date_of_birth,
            biography=domain.biography,
        )
