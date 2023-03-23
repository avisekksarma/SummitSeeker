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
from .models import GuideTrail,Trail,Hire
from django.db.models import Avg
from datetime import datetime,timedelta,date
from utils import log





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
    def post(self,request,trail_id):
        try:
            trail = Trail.objects.get(pk=trail_id)
            # request.data needs to have start_date
            start_date = request.data.get('start_date',None)
            if start_date is None:
                res = makeResponse('start_date is not passed in request body')
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            req_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            req_end_date = req_start_date + timedelta(days = trail.days)
            
            allGuidesOnTrail = GuideTrail.objects.filter(trail=trail)
            possibleGuidesOnTrail = []
            today = date.today()
            for i in allGuidesOnTrail:
                try:
                    Hire.objects.get(trail=trail.id,guide=i.guide.id,tourist=request.user.tourist.id,status='RQ',start_date__gte=today)
                    # this guide on same trail has been requested by me(tourist)
                except:
                    possibleGuidesOnTrail.append(i)
                    
            available_guide_trail = []
            for i in possibleGuidesOnTrail:
                if i.guide.availability == True:
                    hireObjects = Hire.objects.filter(guide = i.guide,status='HR')
                    for j in hireObjects:
                        # log(j.trail.id,delim='&')
                        days = Trail.objects.get(pk=j.trail.id).days
                        # log(days)
                        hired_end_date = j.start_date + timedelta(days=days)
                        if (req_start_date <= hired_end_date and hired_end_date <= req_end_date) or (j.start_date >= req_start_date and j.start_date<=req_end_date):
                            # not available case:
                            # log('broken',delim='%#%')
                            break
                    else:
                    # availablilty = True and not hired in requested date
                        available_guide_trail.append(i)
            serializer = GuideTrailSerializer(available_guide_trail,many=True)
            res = makeResponse('Got all guides',True,serializer.data)
            return Response(res,status= status.HTTP_200_OK)
        except Trail.DoesNotExist:
            res = makeResponse('No such trail exists')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class InitialRequestView(APIView):
    permission_classes = [IsAuthenticated,IsTourist]
    def post(self,request,trail_id,guide_id):
        print(request.path)
        # path is like = /api/trails/1/guides/10/hire
        # TODO: make strict rules on when hiring can be done like stopping repeated hire requests
        try:
            guide_on_trail = GuideTrail.objects.get(guide = guide_id,trail = trail_id)
            guide = Guide.objects.get(pk=guide_id)
            trail = Trail.objects.get(pk=trail_id)
            serializer = HireSerializer(data = request.data)
            if serializer.is_valid():
                hire_obj = serializer.save(guide = guide, trail = trail,tourist = request.user.tourist)
                data = {
                    'hire_id': hire_obj.id,
                    'guide':hire_obj.guide.user.email,
                    'guide_id':hire_obj.guide.id,
                    'tourist':hire_obj.tourist.user.email
                }
                res = makeResponse('Successfully requested to guide',True,data=data)
                
                return Response(res,status=status.HTTP_201_CREATED)
            else:
                res = makeResponse('Invalid data sent in request',validation_error=True,errors=serializer.errors)
                return Response(res,status=status.HTTP_200_OK)

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


