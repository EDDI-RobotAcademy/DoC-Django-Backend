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

    def register(self, request):
        try:
            data = request.data

            reviewTitle = data.get('reviewTitle')
            reviewWriter = data.get('reviewWriter')
            reviewContent = data.get('reviewContent')
            reviewRating  = data.get('reviewRating')
            if request.FILES.get('reviewImage'):
                reviewImage = request.FILES.get('reviewImage')
            else: reviewImage = None

            if not all([reviewTitle, reviewWriter, reviewContent]):
                return Response({'error': '제목, 작성자, 내용은 필수입니다.'},
                                status=status.HTTP_400_BAD_REQUEST)

            registeredReview = self.reviewService.registerReview(reviewTitle, reviewWriter, reviewContent, reviewRating,reviewImage)
            serializer = ReviewSerializer(registeredReview)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print('게시글 등록 과정 중 문제 발생:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

