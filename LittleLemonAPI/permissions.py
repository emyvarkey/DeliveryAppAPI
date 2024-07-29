from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Manager').exists()
    
class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Delivery crew').exists()


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            # If the user is not in any specific group, they are considered a customer
            if not request.user.groups.exists():
                return True
        return False