"""
Player object

Author: Preocts <Preocts#8196>
"""
import logging

from hyapi.authuser import AuthUser


class Player(AuthUser):
    """Player object"""

    logger = logging.getLogger("Player")

    def __init__(self) -> None:
        """Creates an instance of the player class"""
        super().__init__()

        self.is_valid_user

        self.logger.debug("Player object initialized.")

        self.current_player = ""
