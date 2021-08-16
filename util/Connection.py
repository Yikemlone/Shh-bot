from abc import ABC, abstractmethod


class Connection(ABC):

    @staticmethod
    @abstractmethod
    def get_data(data):
        pass
