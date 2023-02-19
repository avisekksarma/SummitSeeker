from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import TravelAgency,ContactNumber
from django.http import HttpResponse
from travelagency.serializers import TravelAgencySerializer
from rest_framework.response import Response

class TravelAgencyList(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        agencies = TravelAgency.objects.all()
        serializer = TravelAgencySerializer(agencies,many=True)
        return Response(serializer.data)

# ------------------ below was for loading data into travelagency model ---------------------
import csv
import os

def fillData(request):
    with open('static/num.csv') as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            agency = TravelAgency.objects.get(pk=row[1])
            ContactNumber.objects.create(contact_num=row[0],travelagency=agency)
    return HttpResponse('hi world')
# -------------------------------------------------------------------------------------------