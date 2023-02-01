from django.urls import path
from .views import PracticeList, PracticeDetail


urlpatterns = [
    path('', PracticeList.as_view(), name='practice_list'),
    path('<int:pk>/', PracticeDetail.as_view(), name='practice_detail'),
]