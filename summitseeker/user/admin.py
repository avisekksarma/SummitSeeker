from django.contrib import admin
from .models import User,Language,Tourist,Guide
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','userType','nationality','gender')


class GuideAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'availability')

admin.site.register(User,UserAdmin)
admin.site.register(Language)
admin.site.register(Tourist)
admin.site.register(Guide,GuideAdmin)