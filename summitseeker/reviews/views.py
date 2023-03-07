from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.permissions import IsTourist, IsGuide
from rest_framework import status
from .serializers import TouristReviewsSerializer, GuideReviewsSerializer, TrailReviewsSerializer
from .models import TouristReviews, GuideReviews, TrailReviews
from utils import log
from django.db.utils import IntegrityError
from utils import makeResponse
from hire.models import Trail


# --------------seeing/getting reviews part--------------------
# You are a tourist or guide, and want to see your reviews
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_my_reviews(request):
    print(request.user.email, request.user.userType)
    if request.user.userType == 'TR':
        # case user is Tourist
        reviews = TouristReviews.objects.filter(
            tourist=request.user.tourist.id)
        serializer = TouristReviewsSerializer(reviews, many=True)
    elif request.user.userType == 'GD':
        # case user is Tourist
        reviews = GuideReviews.objects.filter(guide=request.user.guide.id)
        serializer = GuideReviewsSerializer(reviews, many=True)
    res = makeResponse("Gotten all user's reviews",isSuccess=True,data=serializer.data)
    return Response(res, status=status.HTTP_200_OK)

# You are a tourist and want to see all reviews of a certain guide.


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, IsTourist))
def manage_guide_review(request, pk):
    # the pk is of guide not user in guide table i.e.'id' [ remember that ]
    if request.method == "GET":
        reviews = GuideReviews.objects.filter(guide=pk)
        serializer = GuideReviewsSerializer(reviews, many=True)
        res = makeResponse('Gotten all reviews of requested guide',True,data=serializer.data)
        return Response(res, status=status.HTTP_200_OK)
    elif request.method == "POST":
        # review made by tourist to guide after their hiring/booking confirmed
        request.data['guide'] = pk
        if request.user.userType != 'TR':
            res = makeResponse('Cannot make review on guide by user who is not tourist')
            return Response(res,status=status.HTTP_403_FORBIDDEN)
        serializer = GuideReviewsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(tourist=request.user.tourist)
            except IntegrityError:
                res = makeResponse("You can't review the same guide twice")
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            res = makeResponse('Successfully reviewed of the guide')
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = makeResponse(validation_error=True,errors=serializer.errors)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated, IsTourist))
def have_i_reviewed(request, pk):
    tourist = request.user.tourist
    try:
        review = GuideReviews.objects.get(tourist=tourist, guide=pk)
        response = {
            'reviewed': True
        }
        res = makeResponse('Reviewed till now',isSuccess=True,data=response)
        return Response(res, status=status.HTTP_200_OK)
    except GuideReviews.DoesNotExist as e:
        response = {
            'reviewed': False
        }
        res = makeResponse('Not reviewed till now',isSuccess=True,data=response)
        return Response(res, status=status.HTTP_200_OK)


# get all reviews of a trail,
# post a review in a trail
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def trail_reviews(request, trail_id):
    if request.method == "GET":
        try:
            trail = Trail.objects.get(pk=trail_id)
        except Trail.DoesNotExist:
            res = makeResponse('No such trail exist with given id')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

        reviews = TrailReviews.objects.filter(trail=trail_id)
        serializer = TrailReviewsSerializer(reviews, many=True)
        response = makeResponse(
            message='Gotten all the reviews in the provided trail', isSuccess=True, data=serializer.data)
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = TrailReviewsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                trail = Trail.objects.get(pk=trail_id)
            except Trail.DoesNotExist:
                res = makeResponse(
                'No such trail exist with given id')
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            try:
                review = serializer.save(user=request.user,trail=trail)
                res = makeResponse('Successfully reviewed trail',True,data={
                    'id':review.id
                })
                return Response(res, status=status.HTTP_200_OK)
            except IntegrityError:
                res = makeResponse('You cannot review same trail twice')
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = makeResponse('Error invalid request',validation_error=True,errors=serializer.errors)
            return Response(res,status=status.HTTP_400_BAD_REQUEST)


