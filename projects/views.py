from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.views.generic import ListView, FormView, CreateView


# Create your views here.


class ProjectHome(ListView):
    template_name = 'projects.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get('q')
        projects_all = self.model.objects.prefetch_related('tags', 'project_owner')
        if q:
            tags = Tag.objects.filter(name__icontains=q)
            object_list = projects_all.distinct().filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(project_owner__name__icontains=q) |
                Q(tags__in=tags))
            projects_all = object_list

        return projects_all


class FeedBackView(SingleObjectMixin, FormView):
    template_name = 'single-project.html'
    model = Project
    form_class = ReviewForm
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.project = self.get_object()
        review.owner = self.request.user.profile
        form.save()
        self.get_object().get_vote_count  # property in Project model
        return super(FeedBackView, self).form_valid(form)

    def get_success_url(self):
        return self.request.path


class CreateProject(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'create-project.html'
    form_class = ProjectForm
    success_url = '/account'
    success_message = 'Project has benn created!'

    def form_valid(self, form):
        proj_obj = form.save(commit=False)
        proj_obj.project_owner = self.request.user.profile
        form.save()
        return super(CreateProject, self).form_valid(form)


class UpdateProject(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'slug', 'image', 'description', 'project_owner', 'demo_link', 'source_link', 'tags']
    template_name = 'create-project.html'
    success_url = '/account'


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'delete-project.html'

    def get_success_url(self):
        return reverse('account')


class ProjectByTag(ListView):
    template_name = 'projects.html'
    model = Tag
    context_object_name = 'projects'
    paginate_by = 6



# @login_required(login_url="login")
# def update_project(request, pk):
#     project = Project.objects.get(id=pk)
#     form = ProjectForm(instance=project)
#     if request.method == 'POST':
#         form = ProjectForm(request.POST, instance=project)
#         if form.is_valid():
#             form.save()
#             return redirect('projects')
#     context = {'form': form}
#     return render(request, 'create-project.html', context)


# @login_required(login_url="login")
# def delete_project(request, pk):
#     project = Project.objects.get(id=pk)
#     if request.method == 'POST':
#         project.delete()
#         return redirect('projects')
#     context = {'object': project}
#     return render(request, 'delete-project.html', context)


# def CreateProject(request):
#     profile = request.user.profile
#     form = ProjectForm()
#
#     if request.method == 'POST':
#         form = ProjectForm(request.POST, request.FILES)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.owner = profile
#             project.save()
#
#     context = {'form': form}
#     return render(request, "create-project.html", context)
