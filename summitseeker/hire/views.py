from django.urls import reverse
from .serializers import TrailSerializer
from .models import Trail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from utils import makeResponse
from reviews.models import TrailReviews
from .models import GuideTrail
from .serializers import GuideTrailSerializer
from django.db.models import Avg


class TrailListView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        trails = Trail.objects.all()
        serializer = TrailSerializer(trails,many=True)
        response = makeResponse('Successfully gotten all the trails data',True,serializer.data)
        return Response(response,status = status.HTTP_200_OK)
    
class TrailDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,pk):
        try:
            trail = Trail.objects.get(pk=pk)
            serializer = TrailSerializer(trail)
            reviews = TrailReviews.objects.filter(trail=trail)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            average_difficulty = reviews.aggregate(Avg('difficulty'))['difficulty__avg']
            average_days = reviews.aggregate(Avg('days'))['days__avg']
            serializer1 = dict(serializer.data)
            serializer1['average_rating'] = average_rating
            serializer1['average_difficulty'] = average_difficulty
            serializer1['average_days'] = average_days
            serializer1['links']={
                'guides': reverse('guides-on-a-trail',args=[pk]),
                'reviews': reverse('trail-reviews',args=[pk]),
                # 'reviews':
            }
            # print(serializer.data)
            response = makeResponse('Successfully gotten required trail',True,serializer1)
            return Response(response,status=status.HTTP_200_OK)
        except Trail.DoesNotExist:
            response = makeResponse('Trail with that id does not exist',False,None)
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


class GuidesOnTrail(APIView):
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
