from .serializers import UserSerializer,TouristSerializer,GuideSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import AllowAny,IsAuthenticated
from .permissions import IsTourist,IsGuide
from utils import makeResponse
from utils import log
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

class UserList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
# TODO: make authenticate people disallowed to go in register,login routes
# TODO: may be add features like email otp sending, forgot password, oauth later, check if
# this login/logout is working


# A valid form for registering user
# {
#     "id": 2,
#     "email": "liya@gmail.com",
#     "date_of_birth": "2001-03-22",
#     "gender": "F",
#     "nationality": "AF",
#     "password":"nepalGreat123",
#     "contactNum": 2222678662,
#     "languages": [
#         "CN",
#         "JP"
#     ],
#     "first_name": "liya",
#     "last_name": "pina",
#     "userType":"TR",
#     "experience":"B"
# }


def get_user_types():
    val = User.usertypes
    x =[]
    for i in val:
        x.append(i[0])
    log(x,delim="@")
    return x

def makeTouristData(data):
    x = {}
    if data.get('trekking_experience'):
        x['trekking_experience'] = data.get('trekking_experience')
    # TODO: add future fields here
    return x

def makeGuideData(data):
    log(data,delim="#")
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
                # case: Tourist
                guide_data = makeGuideData(request.data)
                serializer1 =GuideSerializer(data=guide_data)
                if serializer1.is_valid():
                    user = serializer.save()
                    user.is_active = True
                    user.save()
                    serializer1.save(user=user)
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
            makeResponse(message='Errors in validation',validation_error=True, errors=serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes =[AllowAny]
    def post(self,request):
        print(request.data)
        print(type(request.data))
        if not (request.data.get('email',False) and request.data.get('password',False)):
            error ={
                'message':'Email and/or password field is empty.',
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=request.data.get('email'),password=request.data.get('password'))
            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'User login done Successfully',
                    'id': user.id,
                    'email': user.email,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                print("-------raised User doesn't exist error -----------")
                raise User.DoesNotExist
        except User.DoesNotExist:
            error = {
                'message':'Invalid username and/or password',
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

# for now the logout will be handled in client side 
#  by deleting the access,refresh token, but in reality
#  that token is still valid if someone gets it, so best
#  way is blacklisting the tokens ,but for now i leave it.
        
class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_obj_by_pk(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            
            raise 
    def get(self,request,pk):
        user = self.get_obj_by_pk(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

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



class Hello(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        x= request.user.userType
        y = request.user
        data = [
            {'message':f'hi {y} is a {x}!!!'}
        ]
        return Response(data,status.HTTP_200_OK)
    
