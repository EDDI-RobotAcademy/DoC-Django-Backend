from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from review.entity.models import Review
from review.serializers import ReviewSerializer
from review.service.review_service_impl import ReviewServiceImpl


class ReviewView(viewsets.ViewSet):
    queryset = Review.objects.all()
    reviewService = ReviewServiceImpl.getInstance()

    def list(self, request):
        reviewList = self.reviewService.list()
        serializer = ReviewSerializer(reviewList, many=True)
        return Response(serializer.data)

