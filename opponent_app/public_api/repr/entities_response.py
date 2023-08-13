from typing import Optional, List


class EntityResponse:
    """Entity response class."""

    @staticmethod
    def user_publications(publication: Optional[List[dict]] = None) -> dict:
        """Method for creating a dictionary with publications."""
        if isinstance(publication, dict):
            opponent_data = {"data": None, "error": publication}
        else:
            opponent_data = {"data": publication}
        return opponent_data
