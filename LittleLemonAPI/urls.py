from . import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

    #Menu-items endpoints
    path('menu-items', views.MenuItemView.as_view(
        { 'get': 'list',
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
    path('groups/manager/users', views.ManagerGroupView.as_view()),
    path('groups/manager/users/<int:pk>', views.DeleteDeliveryCrewView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewGroupView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeleteDeliveryCrewView.as_view()),

    #url pattern for token generation
    #path('api-token-auth',obtain_auth_token)
]