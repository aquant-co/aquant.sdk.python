from abc import ABC, abstractmethod
from typing import Any


class DatabaseInterface(ABC):
    """
    Abstract contract for database configurations and session management.

    Methods:
        connect(): Establishes the database connection.
        disconnect(): Closes the database connection.
        get_client(): Returns the database client.
    """

    @abstractmethod
    async def connect(self) -> Any:
        """
        Establishes the database connection
        """

    @abstractmethod
    async def disconnect(self) -> Any:
        """
        Closes the database connection and releases resources.
        """

    @abstractmethod
    def get_client(self) -> Any:
        """
        Returns the database client or session for performing operations.

        Returns:
            Any: Client or session instance.
        """
