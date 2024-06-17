from rest_framework import serializers

from board.entity.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['boardId', 'boardTitle', 'boardWriter', 'boardContent', 'boardImage', 'boardRegDate', 'boardUpdDate']
        read_only_fields = ['boardRegDate', 'boardUpdDate']
