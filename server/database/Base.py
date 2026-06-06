from abc import ABC, abstractmethod


class Base(ABC):
    # Abstract database driver interface.
    # New engines (e.g. PostgreSQL) implement this contract later.

    @abstractmethod
    def Connect(self) -> tuple[bool, str]:
        pass

    @abstractmethod
    def Disconnect(self) -> None:
        pass

    @abstractmethod
    def Test(self) -> tuple[bool, str]:
        pass

    @abstractmethod
    def IsActive(self) -> bool:
        pass
