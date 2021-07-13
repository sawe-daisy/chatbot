from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from .models import User
from .forms import RegistrationForm, UserEditForm

def RegisterUser(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            return redirect('login')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration.html', {'form': registerForm})

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         useForm=UserEditForm(request.POST, instance=request.user)
#         if useForm.is_valid():
#             useForm.save()
#             messages.success(request, f'Your account has been updated!')
#         return redirect('profile')
    
#     else:
#         useForm=UserEditForm(instance=request.user)

#     context={
#         'form':useForm,
#     }

#     return render(request, 'index.html', context)


def edit(request):
    if request.method == 'POST':
        userform = UserEditForm(request.POST, instance=request.user)
        print(userform)
        if userform.is_valid():
            print(userform)
            userform.save()
            username= userform.cleaned_data['username']
            print(username)
            first_name= userform.cleaned_data['first_name']
            messages.success(request, f'Your account has been updated!')
            return redirect('index')
        else:
            print("Error")
    else:
        userform = UserEditForm(instance=request.user)
    return render(request,
                  'index.html',
                  {'user_form': userform})


def searchprofile(request): 
    if 'searchUser' in request.GET and request.GET['searchUser']:
        name = request.GET.get("searchUser")
        searchResults = User.search_profile(name)
        message = f'name'
        params = {
            'results': searchResults,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched"
    return render(request, 'search.html', {'message': message})