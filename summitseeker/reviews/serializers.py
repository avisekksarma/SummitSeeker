from rest_framework import serializers
from .models import TouristReviews,GuideReviews

# reviews given to tourist means by currently logged in guide
class TouristReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristReviews
        fields = '__all__'
        extra_kwargs = {
            'guide': {'required': False},
            'tourist':{'required':True},
            'comment':{'required':True},
            'rating':{'required':True}
        }

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating should be in 0-5 range")
        return value

# reviews given to guide means by currently logged in tourist
class GuideReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideReviews
        fields = '__all__'
        extra_kwargs = {
            'guide': {'required': True},
            'tourist':{'required':False},
            'comment':{'required':True},
            'rating':{'required':True}
        }
    def validate_rating(self, value):
        if value<0 or value>5:
            raise serializers.ValidationError("Rating should be in 0-5 range")
        return value