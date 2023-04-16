from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('main:dashboard')
        else: 
            messages.error(request, 'Registration failed')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})




class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserUpdateForm
    profile_form = ProfileUpdateForm
    template_name = 'edit_profile.html'

    def post(self, request, *args, **kwargs):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserUpdateForm(post_data, instance=request.user)
        profile_form = ProfileUpdateForm(post_data, file_data, instance=Profile.objects.get(id=self.kwargs['pk']))
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated, young jedi!")
            return redirect(f'/profile/{request.user.profile.pk}')

        context = self.get_context_data( 
            user_form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)




# @login_required
# def profile(request):
#     if request.method == "POST":
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, 'Your account has been updated!')
#             return redirect('profile')
#         else:
#             u_form = UserUpdateForm(instance=request.user)
#             p_form = ProfileUpdateForm(instance=request.user.profile)
            
#         context = {
#             'u_form': u_form,
#             'p_form': p_form,
#         }
#         return render(request, 'edit_profile.html', context)