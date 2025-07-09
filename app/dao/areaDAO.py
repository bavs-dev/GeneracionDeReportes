# app/dao/area_dao.py
from abc import ABC, abstractmethod

class AreaDAO(ABC):

    @abstractmethod
    def obtener_todos(self, page: int, per_page: int):
        pass

    @abstractmethod
    def obtener_por_id(self, id: int):
        pass

    @abstractmethod
    def guardar(self, nombre: str):
        pass

    @abstractmethod
    def actualizar(self, id: int, nombre: str):
        pass

    @abstractmethod
    def eliminar(self, id: int):
        pass
