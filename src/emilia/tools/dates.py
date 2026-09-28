import datetime

class Dates:
    def __init__(self):
        pass

    def get_current_datetime(self) -> str:
        """
        Use this tool whenever you want to know what time it is right now.

        Args:
            None

        Returns:
            str -> Formatted string containing the exact datetime
        """

        return datetime.datetime.now().strftime(r"%a | %Y/%m/%d -- %H:%M:%S")

