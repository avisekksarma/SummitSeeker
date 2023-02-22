from django.db import models

# reviews given by guides to tourist
class TouristReviews(models.Model):
    guide = models.ForeignKey('user.Guide',on_delete=models.CASCADE)
    tourist = models.ForeignKey('user.Tourist',on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField()

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['guide', 'tourist'], name='unique_guide_tourist'),
        ]
        indexes = [
            models.Index(fields=['guide', 'tourist']),
        ]

    def __str__(self):
        return f'{self.guide.user.email} reviewed {self.tourist.user.email}'


# reviews of guide given by tourists
class GuideReviews(models.Model):
    tourist = models.ForeignKey('user.Tourist',on_delete=models.CASCADE)
    guide = models.ForeignKey('user.Guide',on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField()

    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['tourist','guide'], name='unique_field_guide_tourist'),
        ]
        indexes = [
            models.Index(fields=['tourist','guide']),
        ]
    def __str__(self):
        return f'{self.tourist.user.email} reviewed {self.guide.user.email}'
    
class TrailReviews(models.Model):
    trail = models.ForeignKey('hire.Trail', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField()
    days = models.IntegerField()
    difficulty = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['trail', 'user'], name='unique_field_trail_user'),
        ]
        indexes = [
            models.Index(fields=['trail', 'user']),
        ]

    def __str__(self):
        return f'{self.trail.name} reviewed by {self.user.email}'
