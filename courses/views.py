from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy 
from .models import Course
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View, TemplateResponseMixin
from .forms import ModuleFormSet


# ----- Mixin-Based Architecture -----
class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerMixin:
    """ Mixin to Filter Course by Owner 
    - When used with ListView appear only the courses created by the user
    - When used with CreateView, UpdateView, DeleteView can edit the courses created by the user """
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin:
    """ Mixin to add a user to owner when add a new course """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)    
    
class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')    

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'

# ----- AppViews ----- 
class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'course.add_course'
    
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(View, TemplateResponseMixin):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)   

    def dispatch(self, request, pk,*args, **kwargs):
        self.course = get_object_or_404(Course, id=pk, owner=self.request.user)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course, 'formset':formset})