from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from user.permissions import IsTourist,IsGuide
from rest_framework import status
from .serializers import TouristReviewsSerializer,GuideReviewsSerializer
from .models import TouristReviews,GuideReviews
from utils import log
from django.db.utils import IntegrityError

# --------------seeing/getting reviews part--------------------
# You are a tourist or guide, and want to see your reviews 
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_my_reviews(request):
    print(request.user.email,request.user.userType)
    if request.user.userType == 'TR':
        # case user is Tourist
        reviews = TouristReviews.objects.filter(tourist=request.user.tourist.id)
        serializer = TouristReviewsSerializer(reviews,many=True)
    elif request.user.userType == 'GD':
        # case user is Tourist
        reviews = GuideReviews.objects.filter(guide=request.user.guide.id)
        serializer = GuideReviewsSerializer(reviews,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

# You are a tourist and want to see all reviews of a certain guide.
@api_view(['GET'])
@permission_classes((IsAuthenticated,IsTourist))
def get_guide_review(request,pk):
    # the pk is of guide not user in guide table i.e.'id' [ remember that ]
    reviews = GuideReviews.objects.filter(guide=pk)
    serializer = GuideReviewsSerializer(reviews,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

# --------------creating reviews part--------------------
# review made by tourist to guide after their hiring/booking confirmed
@api_view(['POST'])
@permission_classes((IsAuthenticated,IsTourist))
def make_guide_review(request,pk):
    request.data['guide'] = pk
    serializer = GuideReviewsSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(tourist=request.user.tourist)
        except IntegrityError:
            data = {
                'message':"You can't review the same guide twice",
                'success':False
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        data={
            'message':'Successfully reviewed of the guide',
            'success':True
        }
        return Response(data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,IsTourist))
def have_i_reviewed(request,pk):
    tourist = request.user.tourist
    try:
        review = GuideReviews.objects.get(tourist=tourist,guide = pk)
        data = {
            'message':'Reviewed till now',
            'success':True,
            'reviewed':True
        }
        return Response(data,status=status.HTTP_200_OK)
    except GuideReviews.DoesNotExist as e:
        data = {
            'message':'Not reviewed till now',
            'success':True,
            'reviewed':False
        }
        return Response(data,status=status.HTTP_200_OK)


