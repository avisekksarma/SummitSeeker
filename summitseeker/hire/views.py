from django.urls import reverse
from .serializers import GuideTrailSerializer,HireSerializer,TrailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from user.permissions import IsTourist,IsGuide
from user.models import Guide
from utils import makeResponse
from reviews.models import TrailReviews
from .models import GuideTrail,Trail
from django.db.models import Avg


class TrailListView(APIView):
    # permission_classes = [AllowAny]
    def get(self,request):
        trails = Trail.objects.all()
        serializer = TrailSerializer(trails,many=True)
        response = makeResponse('Successfully gotten all the trails data',True,serializer.data)
        return Response(response,status = status.HTTP_200_OK)
    
class TrailDetailView(APIView):
    # permission_classes = [AllowAny]
    def get(self,request,pk):
        try:
            trail = Trail.objects.get(pk=pk)
            serializer = TrailSerializer(trail)
            reviews = TrailReviews.objects.filter(trail=trail)
            if len(reviews) != 0:
                average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
                average_difficulty = reviews.aggregate(Avg('difficulty'))['difficulty__avg']
            else:
                average_rating = 4
                average_difficulty = 8
            serializer1 = dict(serializer.data)
            serializer1['average_rating'] = average_rating
            serializer1['average_difficulty'] = average_difficulty
            serializer1['links']={
                'guides': reverse('guides-on-a-trail',args=[pk]),
                'reviews': reverse('trail-reviews',args=[pk]),
            }
            # print(serializer.data)
            response = makeResponse('Successfully gotten required trail',True,serializer1)
            return Response(response,status=status.HTTP_200_OK)
        except Trail.DoesNotExist:
            response = makeResponse('Trail with that id does not exist',False,None)
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

class GuidesOnTrail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,trail_id):
        try:
            trail = Trail.objects.get(pk=trail_id)
            objects = GuideTrail.objects.filter(trail=trail)
            serializer = GuideTrailSerializer(objects,many=True)
            res = makeResponse('Got all guides',True,serializer.data)
            return Response(res,status= status.HTTP_200_OK)
        except Trail.DoesNotExist:
            res = makeResponse('No such trail exists')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class Hire(APIView):
    permission_classes = [IsAuthenticated,IsTourist]
    def post(self,request,trail_id,guide_id):
        # path is like = /api/trails/1/guides/10/hire
        # TODO: make strict rules on when hiring can be done like stopping repeated hire requests
        try:
            guide_on_trail = GuideTrail.objects.get(guide = guide_id,trail = trail_id)
            guide = Guide.objects.get(pk=guide_id)
            trail = Trail.objects.get(pk=trail_id)
            serializer = HireSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(guide = guide, trail = trail,tourist = request.user.tourist)
        except GuideTrail.DoesNotExist:
            res = makeResponse('Provided guide does not go in that trial')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
    # getting some data of that guide before submitting form of hiring 
    def get(self,request,trail_id,guide_id):
        try:
            guide_on_trail = GuideTrail.objects.get(guide = guide_id,trail = trail_id)
            data={
                'money_rate':guide_on_trail.money_rate
            }
            res = makeResponse('',True,data)
            return Response(res,status=status.HTTP_200_OK)
        except GuideTrail.DoesNotExist:
            res = makeResponse('Provided guide does not go in that trial')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        