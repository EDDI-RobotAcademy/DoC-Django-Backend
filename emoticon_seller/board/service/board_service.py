from abc import ABC, abstractmethod


class BoardService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def registerBoard(self, boardTitle, boardWriter, boardContent, boardImage):
        pass

    @abstractmethod
    def readBoard(self, boardId):
        pass

    @abstractmethod
    def updateBoard(self, boardId, boardData):
        pass

    @abstractmethod
    def removeBoard(self, boardId):
        pass