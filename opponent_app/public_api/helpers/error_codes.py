

class ErrorCode:
    """Class for error codes. .NET style."""
    @staticmethod
    def parameter_wrong_format(args: str) -> dict:
        """Method for parameter wrong format error code."""
        return {
            'code_number': 404000,
            'code_name': "PARAMETER_WRONG_FORMAT",
            'description': f"Code: 404000. Parameter '{args}' is wrong format.",
            'trace': None
        }

    @staticmethod
    def opponent_not_found() -> dict:
        """Method for opponent not found error code."""
        return {
            'code_number': 303000,
            'code_name': "OPPONENT_NOT_FOUND",
            'description': "Code: 303000. No one opponent not found.",
            'trace': None
        }

    @staticmethod
    def db_connection_error() -> dict:
        """Method for db connection error code."""
        return {
            'code_number': 501000,
            'code_name': "DB_CONNECTION_ERROR",
            'description': "Code: 501000. DB connection error.",
            'trace': None
        }

    @staticmethod
    def internal_unhandled_error() -> dict:
        """Method for internal unhandled error code."""
        return {
            'code_number': 502000,
            'code_name': "INTERNAL_UNHANDLED_ERROR",
            'description': "Code: 502000. Internal unhandled error.",
            'trace': None
        }
