from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("you are logged in. Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == 'post':
        user_form = UserForm(data = request.post)
        profile_form = UserProfileInfoForm(data=request.post)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user

            if 'profile_pick' in request.FILES:
                print('founf it')
                profile.profile_pick = request.FILES['profile_pick']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form =UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})


def user_login(request):
    if request.method == 'post':
        username = request.post.get('username')
        password = request.post.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login & faile!")
            print("username:{} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request,'basic_app/login.html',{})
