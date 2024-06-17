import os

from board.entity.models import Board
from board.repository.board_repository import BoardRepository
from emoticon_seller import settings


class BoardRepositoryImpl(BoardRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Board.objects.all().order_by('boardRegDate')

    def register(self, boardTitle, boardWriter, boardContent, boardImage):
        uploadDirectory = os.path.join(
            settings.BASE_DIR,
            '../../DoC-Vue-Frontend/src/assets/images/uploadImages'
        )
        if not os.path.exists(uploadDirectory):
            os.makedirs(uploadDirectory)
        if boardImage:
            imagePath = os.path.join(uploadDirectory, boardImage.name)
            with open(imagePath, 'wb+') as destination:
                for chunk in boardImage.chunks():
                    destination.write(chunk)

                destination.flush()
                os.fsync(destination.fileno())

            board = Board(
                boardTitle=boardTitle,
                boardWriter=boardWriter,
                boardContent=boardContent,
                boardImage=boardImage.name,
            )
        else:
            board = Board(
                boardTitle=boardTitle,
                boardWriter=boardWriter,
                boardContent=boardContent,
                boardImage=None,
            )
        board.save()
        return board
