from django.db import models
from django.contrib.auth import models as auth_models
from django_countries.fields import CountryField
import datetime

class Language(models.Model):
    # the list is for reference purpose only
    languageList = [
        ('EN','English'),
        ('JP','Japanese'),
        ('GM','German'),
        ('SP','Spanish'),
        ('HD','Hindi'),
        ('FR','French'),
        ('KR','Korean'),
        ('CN','Chinese')
    ]
    languageCode = models.CharField(max_length=2,primary_key=True)
    languageName = models.CharField(max_length=30)
    class Meta:
        ordering = ['languageCode']
    
    def __str__(self):
        return f'{self.languageCode}-{self.languageName}'

class UserManager(auth_models.BaseUserManager):
    def create_user(self,**extra_fields):
        email = extra_fields.pop('email')
        password = extra_fields.pop('password')
        first_name = extra_fields.get('first_name')
        last_name = extra_fields.get('last_name')
        gender = extra_fields.get('gender')
        nationality = extra_fields.get('nationality')
        contactnum = extra_fields.get('contactNum')
        # if not email or not password or not first_name or not last_name or not gender or not nationality or not contactnum:
        #     raise ValueError('Required fields not given when creating user')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
        
    def create_superuser(self,email,password,**extra_fields):

        user = self.create_user(
            email = email,
            password = password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )
        user.save()
        return user

class User(auth_models.AbstractUser):
    gender = [
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
        ('R','Rather not say')
    ]
    usertypes = [
        ('TR','Tourist'),
        ('GD','Guide')
    ]
    username = None
    email = models.EmailField(verbose_name='email',max_length=60,unique=True)
    # avatar = models.ImageField(max_length=300)
    date_of_birth = models.DateField(default=datetime.date.today)
    gender = models.CharField(choices=gender,max_length=2,default='M')
    nationality = CountryField(default='NZ')
    bio = models.TextField(default='',blank=True)
    contactNum = models.BigIntegerField(default=0)
    # avgRating = models.FloatField()
    languages = models.ManyToManyField(Language,blank=True)
    userType = models.CharField(choices = usertypes,max_length=2,default='TR')    
    
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['first_name','last_name','date_of_birth','gender','nationality','contactNum','language']
    # TODO: need to find a way to put language in like create superuser
    REQUIRED_FIELDS = ['first_name', 'last_name','nationality','gender','date_of_birth','userType']

    objects = UserManager()
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_staff

    def has_module_perms(self,app_label):
        return True
    
class Tourist(models.Model):
    exp =[
        ('N','Never Done'),
        ('B','Beginner'),
        ('S','Seasoned'),
        ('P','Professional')
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    trekking_experience = models.CharField(choices=exp,max_length=2,default='B')
    # visited_trails = models

    def __str__(self):
        return self.user.email

class Guide(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    total_trek_count = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email