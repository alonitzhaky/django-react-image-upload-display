from django.urls import path
from .views import product
from . import views 

from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register ),
    path('product/', product ),
    path('product/<int:id>',product),
    path('get_all_images', views.get_product),
    path('upload_image/',views.ImageUpload.as_view()), 
    path('my_product/', views.MyModelView.as_view()),
    path('my_product/<int:pk>/', views.MyModelView.as_view()),
]
