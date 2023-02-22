from .models import Trail,Hire,GuideTrail
from rest_framework import serializers

class TrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trail
        fields = '__all__'

class GuideTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideTrail
        fields = '__all__'
        extra_kwargs = {
            'guide': {'required': True},
            'trail': {'required': True}
        }


class HireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hire
        fields = '__all__'
        extra_kwargs = {
            'tourist': {'required': False},
            'guide': {'required': True},
            'trail': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'deadline': {'required': False},
            'status':{'required':False,'read_only':True},
            'money_rate':{'required':False}
        }

