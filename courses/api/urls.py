from django.urls import path, include 
from . import views 
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet)

app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
    path('subjects/', 
        views.SubjectListView.as_view(), 
        name='subject_list'),
    path('subjects/<pk>/', 
        views.SubjectDetailView.as_view(), 
        name='subject_detail'),
    # path('courses/<pk>/enroll/',
    #     views.CourseEnrollView.as_view(),
    #     name='course_enroll'),
]
