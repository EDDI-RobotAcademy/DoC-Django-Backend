from board.repository.board_repository_impl import BoardRepositoryImpl
from board.service.board_service import BoardService


class BoardServiceImpl(BoardService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__boardRepository = BoardRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return self.__boardRepository.list()

    def registerBoard(self, boardTitle, boardWriter, boardContent, boardImage):
        return self.__boardRepository.register(boardTitle, boardWriter, boardContent, boardImage)

    def readBoard(self, boardId):
        return self.__boardRepository.findByBoardId(boardId)

    def updateBoard(self, boardId, boardData):
        board = self.__boardRepository.findByBoardId(boardId)
        return self.__boardRepository.update(board, boardData)

    def removeBoard(self, boardId):
        return self.__boardRepository.deleteByBoardID(boardId)