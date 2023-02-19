from rest_framework import permissions

class IsTourist(permissions.BasePermission):
    message = 'The user is not a tourist'

    def has_permission(self, request, view):
        return request.user.userType == 'TR'
    

class IsGuide(permissions.BasePermission):
    message = 'The user is not a guide'

    def has_permission(self, request, view):
        return request.user.userType == 'GD'