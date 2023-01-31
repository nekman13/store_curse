from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True, null=True)
    is_verified_email = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f" Объект подтверждения почты - {self.user.email}"

    def send_verification_email(self):
        link = reverse(
            "users:email_verification",
            kwargs={
                "email": self.user.email,
                "code": self.code,
            },
        )
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение почты для пользователя - {self.user.username}"
        message = (
            "Для подтверждение учетной записи для {} перейдите по ссылке {}".format(
                self.user.username, verification_link
            )
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        if now() >= self.expiration:
            return True
        else:
            return False
