from .serializers import UserSerializer,TouristSerializer,GuideSerializer,LanguageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User,Language
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import AllowAny,IsAuthenticated
from .permissions import IsTourist,IsGuide
from utils import makeResponse
from utils import log
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from hire.serializers import GuideTrailSerializer,HireSerializer
from hire.models import Trail,Hire
from django_countries import countries
from datetime import date,timedelta
import copy
from django.db.models import Q



class UserList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
# TODO: make authenticate people disallowed to go in register,login routes
# TODO: may be add features like email otp sending, forgot password, oauth later, check if
# this login/logout is working


class CountriesList(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        countries_dict = dict(countries)
        data = []
        for code, name in list(countries)[:]:
            data.append({
                'countryCode':code,
                'countryName':name
            })
        res = makeResponse('Gotten all countries',True,data=data)
        return Response(res,status=status.HTTP_200_OK)


def get_user_types():
    val = User.usertypes
    x =[]
    for i in val:
        x.append(i[0])
    return x

def makeTouristData(data):
    x = {}
    if data.get('trekking_experience'):
        x['trekking_experience'] = data.get('trekking_experience')
    # TODO: add future fields here
    return x

def makeGuideData(data):
    x = {}
    if data.get('total_trek_count') is not None:
        x['total_trek_count'] = data.get('total_trek_count')
    
    if data.get('availability') is not None:
        x['availability'] = data.get('availability')

    # TODO: add future fields here
    return x


class UserRegister(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        userType = request.data.get('userType')
        print(userType)
        if not (userType and userType in get_user_types()):
            print(userType)
            res = makeResponse('"userType" field not set or set to invalid value',False)
            return Response(res,status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if userType == 'TR':
                # case: Tourist
                tourist_data = makeTouristData(request.data)
                serializer1 =TouristSerializer(data=tourist_data)
                if serializer1.is_valid():
                    user = serializer.save()
                    user.is_active = True
                    user.save()
                    serializer1.save(user=user)
                else:
                    res = makeResponse('Error invalid request',validation_error=True,errors=serializer1.errors)
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            if userType == 'GD':
                # case: Guide
                # TODO: DOING HERE :
                if not request.data.get('trek_routes',None):
                    res = makeResponse(validation_error=True,errors={'trek_routes': ['This field is required']})
                    return Response(res,status=status.HTTP_400_BAD_REQUEST)
                else:
                    trek_routes = request.data.get('trek_routes')

                guide_data = makeGuideData(request.data)
                serializer1 =GuideSerializer(data=guide_data)
                if serializer1.is_valid():
                    user = serializer.save()
                   
                    user.is_active = True
                    user.save()
                    guide = serializer1.save(user=user)
                     # trek routes 
                    for i in trek_routes:
                        # i = { id: 1, money_rate: 2550 }
                        try:
                            trail = Trail.objects.get(pk=i.get('id'))
                        except Trail.DoesNotExist:
                            continue
                        data = {
                            'trail':i.get('id'),
                            'money_rate':i.get('money_rate',1000),
                        }
                        print(data)
                        serializer2 = GuideTrailSerializer(data=data)
                        if serializer2.is_valid():
                            serializer2.save(guide=guide)
                        else:
                            res = makeResponse(
                                'Error invalid request', validation_error=True, errors=serializer2.errors)
                            return Response(res, status=status.HTTP_400_BAD_REQUEST)
                    # 
                else:
                    res = makeResponse('Error invalid request',validation_error=True,errors=serializer1.errors)
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

            # TODO: make user register only by valid email, i.e. say otp
            data = {
                'id':user.id,
                'email':user.email,
                'userType':request.data['userType'],
            }
            res = makeResponse('User registered Successfully',True,data=data)
            return Response(res,status=status.HTTP_201_CREATED)
        # return Response({"done":"yes"},status.HTTP_200_OK)
        else:
            res = makeResponse(message='Errors in validation',validation_error=True, errors=serializer.errors)
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes =[AllowAny]
    def post(self,request):
        print(request.data)
        print(type(request.data))
        if not (request.data.get('email',False) and request.data.get('password',False)):
            res = makeResponse('Email and/or password field is empty.')
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=request.data.get('email'))
            print(request.data.get('password'))
            if user is None:
                print("-------raised User doesn't exist error -----------")
                raise User.DoesNotExist
            successfulLogin = check_password(request.data.get('password',''),user.password)
            if successfulLogin:
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'id': user.id,
                    'email': user.email
                }
                res = makeResponse('User login done Successfully',True,data=data)
                return Response(res, status=status.HTTP_200_OK)
            else:
                # actually password is invalid
                res = makeResponse('Invalid email and/or password')
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # actually email is invalid
            res = makeResponse('Invalid email and/or password')
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

# for now the logout will be handled in client side 
#  by deleting the access,refresh token, but in reality
#  that token is still valid if someone gets it, so best
#  way is blacklisting the tokens ,but for now i leave it.
        
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
            
    def get(self,request,user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            res = makeResponse('No user of that id exists')
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        copy_dict = copy.deepcopy(serializer.data)
        email= copy_dict['email']
        contactNum = copy_dict['contactNum']
        del copy_dict['email']
        del copy_dict['contactNum']
        today = date.today()
        if request.user.userType == 'TR' and user.userType == 'GD':
            all_hires = Hire.objects.filter(tourist=request.user.tourist.id,guide=user.guide.id,start_date__gte=today)
            hire_serializer = HireSerializer(all_hires,many=True)
            for i in hire_serializer.data:
                log(i,delim='*&')
                if i['status']=='HR':
                    copy_dict['email'] = email
                    copy_dict['contactNum'] = contactNum
                    break
        elif request.user.userType == 'GD' and user.userType == 'TR':
            all_hires = Hire.objects.filter(
                tourist=user.tourist.id, guide=request.user.guide.id, start_date__gte=today)
            hire_serializer = HireSerializer(all_hires, many=True)
            for i in hire_serializer.data:
                if i['status'] == 'HR':
                    copy_dict['email'] = email
                    copy_dict['contactNum'] = contactNum
                    break
        res = makeResponse('Gotten user detail',True,data=copy_dict)
        return Response(res,status=status.HTTP_200_OK)

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserSerializer(request.user)
        serializer1 = dict(serializer.data)
        if request.user.userType == 'TR':
            serializer1['trekking_experience'] = request.user.tourist.trekking_experience
        elif request.user.userType == 'GD':
            serializer1['total_trek_count'] = request.user.guide.total_trek_count
            serializer1['availability'] = request.user.guide.availability
        res = makeResponse('Shown profile of user',True,data=serializer1)
        return Response(res,status=status.HTTP_200_OK)

# return available languages
class LanguageManager(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        l = Language.objects.all()
        languages = LanguageSerializer(l,many=True)
        res = makeResponse('Got all languages',True,data=languages.data)
        return Response(res,status=status.HTTP_200_OK)

class Hello(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        x= request.user.userType
        y = request.user
        data = [
            {'message':f'hi {y} is a {x}!!!'}
        ]
        return Response(data,status.HTTP_200_OK)

# class RecommendedTrail(APIView):
#     permission_classes = [IsAuthenticated,IsTourist]
#     def get(self,request):
#         hireObjects = Hire.objects.filter(tourist = request.user.tourist.id,status='HR')
#         min = 99999
#         max = -99999
#         for i in hireObjects:
#             if i.trail.days < min:
# 

class CancelRequest(APIView):
    permission_classes = [IsAuthenticated,IsTourist]
    def get(self,request,hire_id):
        try:
            hireObj = Hire.objects.get(pk=hire_id)
            if hireObj.status == 'RQ':
                hireObj.delete()
                res = makeResponse('Succesfully cancelled request',True)
                return Response(res,status=status.HTTP_200_OK)
            else:
                res = makeResponse('No request sent in that hire id')
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
        except:
            res = makeResponse('Hire object of that id does not exist')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class HireAcceptOrRejectView(APIView):
    permission_classes = [IsAuthenticated, IsGuide]
    def post(self, request,hire_id):
        try:
            hireObj = Hire.objects.get(pk=hire_id)
            sent_status = request.data.get('status')
            if sent_status and (sent_status == 'AC' or sent_status=='RJ'):
                hireObj.status = sent_status
                hireObj.save()
                serializer = HireSerializer(hireObj)
                res = makeResponse('Updated successfully',isSuccess=True,data=serializer.data)
                return Response(res,status=status.HTTP_200_OK)
            else:
                res = makeResponse('Send "AC" or "RJ" in status')
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
        except:
            res = makeResponse('Hire object of that id does not exist')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class HireTheGuide(APIView):
    permission_classes = [IsAuthenticated, IsTourist]
    def post(self, request):
        try:
            hire_id = request.data.get('hire_id')
            if hire_id:
                hireObj = Hire.objects.get(pk=hire_id)
                hireObj.status = 'HR'
                hireObj.save()
                serializer = HireSerializer(hireObj)
                res = makeResponse('Guide Hired Successfully',isSuccess=True,data=serializer.data)
                return Response(res,status=status.HTTP_200_OK)
            else:
                res = makeResponse('Hire id not provided in body')
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except Hire.DoesNotExist:
            res = makeResponse('Hire object of that id does not exist')
            return Response(res,status=status.HTTP_400_BAD_REQUEST)




class Notification(APIView):
    # sends all inquired and accepted guides for that user
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.userType=='TR':
            today = date.today()
            all_hires = Hire.objects.filter(tourist=request.user.tourist.id,start_date__gte=today)
            serializer = HireSerializer(all_hires,many=True)
            accepted = []
            others = []
            for i in serializer.data:
                if i['status'] == 'AC':
                    accepted.append(i)
                else:
                    others.append(i)
            data = {
                'Accepted':accepted,
                'All':others
            }

            #  end_date <= today <= end_date + 3 days from end_date
            #  now computation for which guides and trails the tourist can review
            possible_reviews = Hire.objects.filter(tourist=request.user.tourist.id,end_date__lte=today,status='HR')
            actual_reviews = []
            for i in possible_reviews:
                end_date_plus_three = i.end_date + timedelta(days=3)
                if today <= end_date_plus_three:
                    actual_reviews.append(i)
            
            trails = []
            guides = []
            for j in actual_reviews:
                trails.append({'id':j.trail.id,'trail_name':j.trail.name})
                guide_user = j.guide.user
                guide_full_name = guide_user.first_name + " "+ guide_user.last_name
                guides.append({'id':j.guide.id,'guide_full_name':guide_full_name})

            data['trails'] = trails
            data['guides'] = guides

            response = makeResponse('Successfully gotten all notification',True,data)
            return Response(response,status = status.HTTP_200_OK)
        else:
            today = date.today()
            all_hires = Hire.objects.filter(guide=request.user.guide.id,start_date__gte=today)
            serializer = HireSerializer(all_hires,many=True)
            requested = []
            acceptedorrejected = []
            hired= []
            for i in serializer.data:
                if i['status'] == 'RQ':
                    requested.append(i)
                elif i['status'] == 'AC' or i['status'] == 'RJ':
                    acceptedorrejected.append(i)
                else:
                    hired.append(i)
            data = {
                'Requested':requested,
                'Responded':acceptedorrejected,
                'Hired':hired
            }

            # ------------------
            #  end_date <= today <= end_date + 3 days from end_date
            #  now computation for which tourists and trails the guide can review
            possible_reviews = Hire.objects.filter(
                guide=request.user.guide.id, end_date__lte=today, status='HR')
            actual_reviews = []
            for i in possible_reviews:
                end_date_plus_three = i.end_date + timedelta(days=3)
                if today <= end_date_plus_three:
                    actual_reviews.append(i)

            trails = []
            tourists = []
            for j in actual_reviews:
                trails.append({'id': j.trail.id, 'trail_name': j.trail.name})
                tourist_user = j.tourist.user
                tourist_full_name = tourist_user.first_name + " " + tourist_user.last_name
                tourists.append(
                    {'id': j.tourist.id, 'tourist_full_name': tourist_full_name})

            data['trails'] = trails
            data['tourists'] = tourists

            # ------------------

            response = makeResponse('Successfully gotten all notification',True,data)
            return Response(response,status = status.HTTP_200_OK)