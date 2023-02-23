from .models import Trail,Hire,GuideTrail
from rest_framework import serializers

class TrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trail
        fields = ['id','name','image']

class GuideTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideTrail
        fields = '__all__'
        extra_kwargs = {
            'guide': {'required': True},
            'trail': {'required': True}
        }
        # depth= 1

from datetime import datetime,timedelta

class HireSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        print('-----------------fdfda-------------')
        print(validated_data)
        print(validated_data['trail'])
        # Trail.objects.get(pk=validated_data['trail'])
        validated_data['end_date'] = validated_data['start_date']+timedelta(days = validated_data['trail'].days)
        print(validated_data)
        print('-----------------fdfda-------------')
        return Hire.objects.create(**validated_data)
    
    class Meta:
        model = Hire
        fields = '__all__'
        # guide, trail will be in path
        # tourist is the request making user
        # end date is start date +  average duration of that trail
        # deadline is by default = 3 days from initial request book
        # money_rate is by default base_money_rate but if hired then average of that guide
        # on that trail
        extra_kwargs = {
            'tourist': {'required': False, 'read_only':True},
            'guide': {'required': False, 'read_only': True},
            'trail': {'required': False, 'read_only': True},
            'start_date': {'required': True},
            'end_date': {'required': False,'read_only':True},
            'deadline': {'required': True},
            'status':{'required':True},
            'money_rate':{'required':True}
        }

    
