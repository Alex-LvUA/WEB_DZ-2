
from abc import ABC, abstractmethod
"""
тут знаходяться класи які потрібні в інших модулях
"""
class Mod(ABC):
    @staticmethod
    @abstractmethod
    def call():
        pass