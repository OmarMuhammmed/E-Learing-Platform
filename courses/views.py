from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy 
from .models import Course, Module, Content
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View, TemplateResponseMixin
from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JSONResponseMixin

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
    
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    object = None

    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(model, exclude=[
                                                'owner',
                                                'order',
                                                'created',
                                                'updated',
                                                ])
        return form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, 
                                        id=module_id, 
                                        course__owner=self.request.user)
        self.model = self.get_model(model_name)
        if id:
            self.object = get_object_or_404(self.model, 
                                            id=id, 
                                            owner=self.request.user)
        return super().dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.object)
        return self.render_to_response({'form': form, 
                                        'object': self.object})
    
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.object,   
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = self.request.user
            obj.module = self.module
            obj.save()
            if not id : # Create Content 
                Content.objects.create(module=self.module,
                                       item=obj)
                
            return redirect('module_content_list', 
                            module_id=self.module.id)
        
        return self.render_to_response({'form': form, 
                                        'object': self.object})
    
class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, 
                                    id=id, 
                                    module__course__owner=request.user)  
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module_id=module.id)  
    
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                 id=module_id,
                                 course__owner=request.user)
        return self.render_to_response({'module':module})  

class ModuleOrderView(CsrfExemptMixin, JSONResponseMixin, View):      
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)

        return self.render_json_response({'saved': 'OK'})    
    

class ContentOrderView(CsrfExemptMixin, JSONResponseMixin, View):    
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)

        return self.render_json_response({'saved': 'OK'})