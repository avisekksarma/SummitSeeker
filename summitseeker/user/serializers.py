from rest_framework import serializers
from .models import User,Language,Tourist,Guide


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    def create(self,validated_data):
        language_data = validated_data.pop('languages')
        user = User.objects.create(**validated_data)
        user.languages.add(*language_data)
        return user
    # TODO: For now, update is not supported
    
    class Meta:
        model = User
        extra_kwargs = {
            'email': {'required': True},
            'date_of_birth': {'required': True},
            'gender': {'required': True},
            'nationality': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'contactNum': {'required': True},
            'languages': {'required': True},
            'userType': {'required': True},
        }
        fields = ['id', 'email', 'date_of_birth',
                'gender', 'nationality', 'password',
                'contactNum',
                'languages',
                'first_name',
                'last_name','userType']
    
class TouristSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        print(validated_data)
        return Tourist.objects.create(**validated_data)
    class Meta:
        model = Tourist
        fields = ['id','user','trekking_experience']
        extra_kwargs = {
            'user': {'required': False}
        }


class GuideSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        return Guide.objects.create(**validated_data)
    def to_internal_value(self, data):
        print('-------')
        print(data)
        print('-------')
        return super().to_internal_value(data)
    class Meta:
        model = Guide
        fields = ['id','user','total_trek_count','availability']
        extra_kwargs = {
            'user': {'required': False}
        }
