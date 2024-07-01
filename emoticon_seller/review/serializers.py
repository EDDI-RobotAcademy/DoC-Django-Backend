from rest_framework import serializers

from review.entity.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewId', 'reviewTitle', 'reviewWriter', 'reviewContent', 'reviewImage','reviewRating' ,'reviewRegDate', 'reviewUpdDate']
        read_only_fields = ['reviewRegDate', 'reviewUpdDate']
