from django.db import models


class Board(models.Model):
    boardId = models.AutoField(primary_key=True)
    boardTitle = models.CharField(max_length=128, null=False)
    boardWriter = models.CharField(max_length=32, null=False)
    boardContent = models.TextField()
    boardImage = models.CharField(max_length=100, null=True)
    boardRegDate = models.DateTimeField(auto_now_add=True)
    boardUpdDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.boardTitle

    class Meta:
        db_table = 'board'
