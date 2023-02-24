from django.db import models

class Trail(models.Model):
    name = models.CharField(max_length=30)
    mapImage = models.ImageField(upload_to='trailphotos/mapImage/',max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='trailphotos/',max_length=200,null=True,blank=True)
    reviews = models.ManyToManyField('user.User',through='reviews.TrailReviews')
    days = models.IntegerField()
    # Following will be gotten from aggregate funcs. on another table.
    # average_days = models.IntegerField()
    # average_difficulty = models.IntegerField()
    # average_rating = models.FloatField()

    def __str__(self):
        return f'{self.name}'
    

class GuideTrail(models.Model):
    guide = models.ForeignKey('user.Guide',on_delete= models.CASCADE)
    trail = models.ForeignKey('Trail',on_delete=models.CASCADE)
    money_rate = models.FloatField(default=1000)
    # count,avg_rate,others will be grabbed from using aggregate function on
    # hire table
    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['guide','trail'], name='unique_field_guide_trail'),
        ]
        indexes = [
            models.Index(fields=['guide','trail']),
        ]
    def __str__(self):
        return f'{self.guide.user.email} Guide in Trail --> {self.trail.name}'

class Hire(models.Model):
    cases = [
        ('RQ','Requested'),
        ('AC','Accepted'),
        ('RJ','Rejected'),
        ('NG','Negotiate'),
        ('HR','Hired')
    ]
    # TODO: make sure to manage cases when same tourist requests same guide on same trail , other cases in like same time maybe
    tourist = models.ForeignKey('user.Tourist',on_delete=models.CASCADE)
    guide = models.ForeignKey('user.Guide',on_delete=models.CASCADE)
    trail = models.ForeignKey('Trail',on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    # default = 3 days from initial book time.
    deadLine = models.IntegerField(default = 3)
    status = models.CharField(choices = cases,max_length=2)
    money_rate = models.FloatField()

    def __str__(self):
        return f'{self.tourist.user.email} is hiring {self.guide.user.email} on {self.trail.name} in status = {self.status}'
