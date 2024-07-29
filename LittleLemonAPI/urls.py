from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('categories', views.CategoriesView.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    )),
    path('categories/<int:pk>', views.CategoriesView.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }
    )),

    #Menu-items endpoints
    path('menu-items', views.MenuItemView.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    )),
    path('menu-items/<int:pk>', views.MenuItemView.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }
    )),

    #User group management endpoints
    path('groups/manager/users', views.ManagerGroupManagementViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    )),
    path('groups/manager/users/<int:pk>/', views.ManagerGroupManagementViewSet.as_view(
        {
            'delete': 'destroy',
        }
        
    )),

    path('groups/delivery-crew/users', views.DeliveryCrewGroupManagementViewSet.as_view(
        {
            'get': 'list', 
            'post': 'create',
        }
    )),
    path('groups/delivery-crew/users/<int:pk>/', views.DeliveryCrewGroupManagementViewSet.as_view(
        {
            'delete': 'destroy',
            }
    )),

    #Cart management endpoints 
    path('cart/menu-items',views.CartView.as_view()),

    #Order management endpoints
    path('orders',views.OrderView.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    )),
    path('orders/<int:pk>', views.OrderView.as_view(
                {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }
    )),

]



