from typing import Optional, List


class EntityResponse:
    @staticmethod
    def user_publications(
        publication: Optional[List[dict, ]] = None
    ) -> dict:
        if isinstance(publication, dict):
            opponent_data = {
                'data': None,
                'error': publication
            }
        else:
            opponent_data = {
                'data': publication
            }
        return opponent_data
