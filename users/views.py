from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy
from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserChangeProfileForm
from django.contrib.auth.decorators import login_required


# Create your views here.



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'Вы успешно авторизованы!')
                return redirect(reverse_lazy('index'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect(reverse_lazy('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'users/registration.html', context)
@login_required()
def profile(request):
    if request.method == 'POST':
        form = UserChangeProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserChangeProfileForm(instance=request.user)


    context={
    'form': form,
    'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/pofile.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'Вы успешно вышли из профиля!')
    return redirect(reverse_lazy('index'))
