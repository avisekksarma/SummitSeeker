from rest_framework import serializers 
from .models import TravelAgency,ContactNumber

class TravelAgencySerializer(serializers.ModelSerializer):
    # contactnumbers = serializers.PrimaryKeyRelatedField(queryset=ContactNumber.objects.all(),many=True)
    cn = serializers.StringRelatedField(many=True)
    class Meta:
        model = TravelAgency
        fields = ['name','address','num_of_trips','duration','price','average_rating','cn']

