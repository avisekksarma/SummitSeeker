from django.http import HttpResponse
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import AllowAny,IsAuthenticated
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

class UserList(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
# TODO: make authenticate people disallowed to go in register,login routes
class UserRegister(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        data = []
        if serializer.is_valid():
            user = serializer.save()
            user.is_active =True
            user.save()
            # TODO: make user register only by valid email, i.e. say otp
            data ={
                'message':'User registered Successfully',
                'id':user.id,
                'username':user.username,
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes =[AllowAny]
    def post(self,request):
        print(request.data)
        print(type(request.data))
        if not (request.data.get('username',False) and request.data.get('password',False)):
            error ={
                'message':'Username and/or password field is empty.',
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=request.data.get('username'),password=request.data.get('password'))
            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'User login done Successfully',
                    'id': user.id,
                    'username': user.username,
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                print("-------raised User doesn't exist -----------")
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
    def get_obj_by_pk(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        user = self.get_obj_by_pk(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

