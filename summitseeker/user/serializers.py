from rest_framework import serializers
from .models import User,Language

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
        }
        fields = ['id', 'email', 'date_of_birth',
                'gender', 'nationality', 'password',
                'contactNum',
                'languages',
                'first_name',
                'last_name']
    
        