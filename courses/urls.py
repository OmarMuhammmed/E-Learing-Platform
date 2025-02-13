from django.urls import path 
from . import views

urlpatterns = [
    path('list/',
        views.ManageCourseListView.as_view(),
        name='manage_course_list'),
    path('create/',
        views.CourseCreateView.as_view(),
        name='course_create'),
    path('<pk>/update/',
        views.CourseUpdateView.as_view(),
        name='course_update'), 
    path('<pk>/delete/',
        views.CourseDeleteView.as_view(),
        name='course_delete'),       
]