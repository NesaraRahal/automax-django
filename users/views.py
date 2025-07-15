from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, ProfileForm, LocationForm


#importing View (inheritance) for class based views
from django.views import View
# Create your views here.

def login_view(request):    
    if request.method == 'POST':
        login_form = AuthenticationForm(request = request, data = request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            #print(user)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}')
                return redirect('home')
            else:
                messages.error(request, f'An error occured while login')
        else:
            messages.error(request, f'An error occured while login')
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    
    return render(request, 'views/login.html', {'login_form' : login_form} )


#Logout function
@login_required
def logout_view(request):
    logout(request)
    return redirect('main') 


#There are 2 types of views as function based views and class bases views
#wE USE FUNCTION BASED VIEW WHEN WE HAVE A LESS COMPLEX LOGIC OR HAVE JUST ONE OR TWO REQUEST METHODS(GET / POST)
#WE USE CLASS BASED VIEW WHEN WE HAVE COMPLEC LOGIC OR CONTAIN DIFFERENT REQUEST METHODS

#FINCTION BASED VIEW FOR register_view (Commented one)
"""def register_view(request):
    register_form = UserCreationForm()
    return render(request, 'views/register.html', {'register_form' : register_form})"""

class RegisterView(View):
    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'views/register.html',{'register_form' : register_form})
    
    def post(self, request):
        register_form = UserCreationForm(data = request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(request, f'User { user.username } registered successfully')
            return redirect('home')  
        else:
            messages.error(request, f'An occured while Register')
            return render(request, 'views/register.html', {'register_form' : register_form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)
        return render(request, 'views/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'location_form': location_form});
    
    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        location_form = LocationForm(request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, f'Profile Updated Successfully!')
        else: 
            messages.success(request, f'Error occured while updating the profile')

        return render(request, 'views/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'location_form': location_form});
