from rest_framework.permissions import BasePermission

class IsManagerOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return request.user and request.user.groups.filter(name='Manager').exists()
    
class IsDeliveryCrewOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return request.user and request.user.groups.filter(name='Delivery crew').exists()

