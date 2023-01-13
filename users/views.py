from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView, FormView
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm, LoginUser
from .models import Profile, Skill


class HomeProfile(ListView):
    template_name = 'users/profiles.html'
    model = Profile
    context_object_name = 'profiles'
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get('q')
        profiles_all = self.model.objects.select_related('user').prefetch_related('skills')
        if q:
            skills = Skill.objects.distinct().filter(name__icontains=q)
            profile_list = profiles_all.distinct().filter(
                Q(name__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(skills__in=skills))

            profiles_all = profile_list
        return profiles_all


class UserProfile(TemplateView):
    template_name = 'users/user-profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        profile = Profile.objects.get(username=self.kwargs['username'])
        context['profile'] = profile
        context['main_skills'] = profile.skills.all()
        context['extra_skills'] = profile.skills.all()
        return context


class ProfileBySkill(ListView):
    template_name = "users/profiles.html"
    model = Skill
    context_object_name = 'profiles'
    paginate_by = 6

    def get_queryset(self):
        skill = get_object_or_404(Skill, slug=self.kwargs['skill_slug'])
        profiles = Profile.objects.select_related('user').prefetch_related('skills').filter(skills__in=[skill])
        return profiles


class CustomLoginUser(LoginView, View):
    page = 'login'  # for check in template
    form_class = LoginUser
    template_name = 'users/login_register.html'

    def get_success_url(self):
        return reverse_lazy('profiles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page'] = self.page
        return context


class RegisterUser(CreateView):
    page = 'register'  # for check in template
    template_name = 'users/login_register.html'
    form_class = CustomUserCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page'] = self.page
        return context

    def get_success_url(self):
        return reverse_lazy('projects')


class UserAccount(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        profile = self.request.user.profile
        context['profile'] = profile.user.profile
        context['skills'] = profile.skills.all()
        context['projects'] = profile.projects.all()
        return context


class EditAccount(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/profile_form.html'
    model = Profile
    form_class = ProfileForm
    success_url = '/account'
    success_message = 'Account info changed!'

    def get_object(self):
        return self.model.objects.get(id=self.request.user.profile.id)

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        form = ProfileForm(instance=profile)
        context = super().get_context_data()
        context['profile'] = profile
        context['form'] = form
        return context


class SkillCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/skill_form.html'
    model = Skill
    form_class = SkillForm
    success_url = '/account'
    success_message = 'Skill added!'

    def form_valid(self, form):
        profile = self.request.user.profile
        form.save()
        profile.skills.add(form.instance)
        return super().form_valid(form)


class SkillUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/skill_form.html'
    model = Skill
    form_class = SkillForm
    success_url = '/account'
    success_message = 'Skill changed!'


class SkillDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Skill
    success_url = '/account'
    template_name = 'users/skills.html'
    success_message = 'Skill removed from user!'

    # removing skill related with profile. Not delete it Skill model

    def delete(self, request, *args, **kwargs):
        skill = request.user.profile.skills.get(slug=self.kwargs['slug'])
        return request.user.profile.skills.remove(skill)


class InboxView(LoginRequiredMixin, TemplateView):
    template_name = 'users/inbox.html'

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        message_requests = profile.messages.all()
        unread_count = message_requests.filter(is_read=False).count()
        context = super(InboxView, self).get_context_data()
        context['message_requests'] = message_requests
        context['unread_count'] = unread_count
        return context


class CreateMessage(SingleObjectMixin, FormView, SuccessMessageMixin):
    model = Profile
    template_name = 'users/message_form.html'
    form_class = MessageForm
    context_object_name = 'recipient'
    success_url = '/login'

    def get_object(self, queryset=None):
        return self.model.objects.get(username=self.kwargs['username'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            sender = self.request.user.profile
        except:
            sender = None
        message = form.save(commit=False)
        message.sender = sender
        message.recipient = self.get_object()

        if sender:
            message.name = sender.name
            message.email = sender.email
        message.save()
        return super(CreateMessage, self).form_valid(form)

class MessageView(TemplateView):
    template_name = 'users/messages.html'

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        message = profile.messages.get(id=self.kwargs['pk'])
        context = super(MessageView, self).get_context_data()
        context['message'] = message
        if not message.is_read:
            message.is_read = True
            message.save()
        return context


class UserLogout(LogoutView):
    template_name = 'users/login_register.html'

# FBV

# def create_message(request, username):
#     recipient = Profile.objects.get(username=username)
#     form = MessageForm()
#
#     try:
#         sender = request.user.profile
#     except:
#         sender = None
#
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = sender
#             message.recipient = recipient
#
#             if sender:
#                 message.name = sender.name
#                 message.email = sender.email
#             message.save()
#
#             messages.success(request, 'Your message has been sent')
#             return redirect('user-profile', username=recipient.username)
#
#     context = {'recipient': recipient, 'form': form, }
#     return render(request, 'users/message_form.html', context)

# LOGOUT_REDIRECT_URL = 'login' in settings.py

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['page'] = 'login'
    #     return context


# @login_required(login_url='login')
# def view_message(request, pk):
#     profile = request.user.profile
#     message = profile.messages.get(id=pk)
#     if message.is_read == False:
#         message.is_read = True
#         message.save()
#     context = {'message': message}
#     return render(request, 'users/messages.html', context)


# @login_required(login_url='login')
# def inbox(request):
#     profile = request.user.profile
#     message_requests = profile.messages.all()
#     unread_count = message_requests.filter(is_read=False).count()
#     context = {
#         'messageRequests': message_requests,
#         'unreadCount': unread_count
#     }
#     return render(request, 'users/inbox.html', context)

# def user_profile(request, username):
#     profile = Profile.objects.get(username=username)
#     main_skills = profile.skills.all()
#     extra_skills = profile.skills.all()
#     context = {'profile': profile, 'main_skills': main_skills,
#                "extra_skills": extra_skills}
#     return render(request, 'users/user-profile.html', context)


# @login_required(login_url='login')
# def edit_account(request):
#     profile = request.user.profile
#     form = ProfileForm(instance=profile)
#
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#
#             return redirect('account')
#
#     context = {'form': form, 'profile': profile}
#     return render(request, 'users/profile_form.html', context)


# @login_required(login_url='login')
# def user_account(request):
#     profile = request.user.profile
#
#     skills = profile.skills.all()
#     projects = profile.project_set.all()
#
#     context = {'profile': profile, 'skills': skills, 'projects': projects}
#
#     return render(request, 'users/account.html', context)


# def logout_user(request):
#     logout(request)
#     messages.info(request, 'you are logged out')
#     return redirect('login')


# def profiles_by_skill(request, skill_slug):
#     skill = get_object_or_404(Skill, slug=skill_slug)
#     profiles = Profile.objects.select_related('user').prefetch_related('skills').filter(skills__in=[skill])
#     context = {
#         "profiles": profiles
#     }
#     return render(request, "users/profiles.html", context)

# @login_required(login_url='login')
# def update_skill(request, skill_slug):
#     profile = request.user.profile
#     skill = profile.skills.get(slug=skill_slug)
#     form = SkillForm(instance=skill)
#
#     if request.method == 'POST':
#         form = SkillForm(request.POST, instance=skill)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Skill changed')
#             return redirect('account')
#
#     context = {'form': form}
#     return render(request, 'users/skill_form.html', context)


# @login_required(login_url='login')
# def delete_skill(request, skill_slug):
#     if request.method == 'DELETE':
#         skill = request.user.profile.skills.get(slug=skill_slug)
#         request.user.profile.skills.remove(skill)
#         messages.success(request, 'skill was successfully removed ')
#         skills = request.user.profile.skills.all()
#         return render(request, 'users/skills.html', {'skills': skills})


# @login_required(login_url='login')
# def create_skill(request):
#     profile = request.user.profile
#     form = SkillForm()
#
#     if request.method == 'POST':
#         form = SkillForm(request.POST)
#         if form.is_valid():
#             skill = form.save(commit=False)
#             skill_slug = request.POST.get('slug')
#             skill_description = request.POST.get('description')
#             profile.skills.get_or_create(name=skill, slug=skill_slug, description=skill_description)
#             messages.success(request, 'Skill added')
#             return redirect('account')
#
#     context = {'form': form}
#     return render(request, 'users/skill_form.html', context)
