from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserChangeProfileForm
from django.contrib.auth.decorators import login_required

from users.models import User


# Create your views here.

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserProfileView(UpdateView):
    template_name = 'users/pofile.html'
    model = User
    form_class = UserChangeProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id, ))

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')



def logout(request):
    auth.logout(request)
    messages.success(request, 'Вы успешно вышли из профиля!')
    return redirect(reverse_lazy('index'))




# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, 'Вы успешно авторизованы!')
#                 return redirect(reverse_lazy('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)


#
# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрированы!')
#             return redirect(reverse_lazy('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/registration.html', context)
# @login_required()
# def profile(request):
#     if request.method == 'POST':
#         form = UserChangeProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse_lazy('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserChangeProfileForm(instance=request.user)
#
#
#     context={
#     'form': form,
#     'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/pofile.html', context)