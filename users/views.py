from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import CommonMixin
from users.forms import UserChangeProfileForm, UserLoginForm, UserRegistrationForm
from users.models import EmailVerification, User

# Create your views here.


class EmailVerificationView(CommonMixin, TemplateView):
    title = "Подтверждение почты"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if (
            email_verifications.exists()
            and not email_verifications.first().is_expired()
        ):
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy("products:index"))


class UserLoginView(CommonMixin, SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_message = "Добро пожаловать!"
    title = "Авторизация"


class UserProfileView(CommonMixin, UpdateView):
    template_name = "users/pofile.html"
    model = User
    form_class = UserChangeProfileForm
    title = "Личный кабинет"

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.request.user.id,))


class UserRegistrationView(CommonMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегистрированы!"
    title = "Регистрация"


def logout(request):
    auth.logout(request)
    messages.success(request, "Вы успешно вышли из профиля!")
    return redirect(reverse_lazy("index"))


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
