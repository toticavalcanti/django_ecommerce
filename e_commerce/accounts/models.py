from django.db import models
import logging

logger = logging.getLogger('accounts')  # Logger configurado para o app accounts

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Gerenciador de usuários
class UserManager(BaseUserManager):

    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False, is_verified=False):
        """
        Cria e retorna um usuário regular.
        """
        if not email:
            logger.error("Falha ao criar usuário: E-mail é obrigatório.")
            raise ValueError("O Usuário deve ter um endereço de email!")
        if not password:
            logger.error("Falha ao criar usuário: senha necessária.")
            raise ValueError("O Usuário deve ter uma senha!")

        user_obj = self.model(
            full_name=full_name,
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)  # Configura a senha
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.is_verified = is_verified
        user_obj.save(using=self._db)
        logger.info(f"Usuário criado com sucesso: {email}")
        return user_obj

    def create_staffuser(self, email, full_name=None, password=None):
        """
        Cria e retorna um usuário da equipe.
        """
        logger.info(f"Tentando criar um usuário de equipe: {email}")
        user = self.create_user(
            email=email,
            full_name=full_name,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=False,
            is_verified=False
        )
        logger.info(f"Usuário da equipe criado com sucesso: {email}")
        return user

    def create_superuser(self, email, full_name=None, password=None):
        """
        Cria e retorna um superusuário.
        """
        logger.info(f"Tentando criar superusuário: {email}")
        user = self.create_user(
            email=email,
            full_name=full_name,
            password=password,
            is_active=True,
            is_staff=True,
            is_admin=True,
            is_verified=True
        )
        logger.info(f"Superusuário criado com sucesso: {email}")
        return user


# Modelo de usuário personalizado
class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)  # Pode fazer login
    staff = models.BooleanField(default=False)  # Usuário da equipe, não superusuário
    admin = models.BooleanField(default=False)  # Superusuário
    is_verified = models.BooleanField(default=False, help_text="Indica se o email do usuário foi verificado.")
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # Campo principal para login
    REQUIRED_FIELDS = []  # Campos obrigatórios além do email e senha

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name or self.email

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


# Modelo para e-mails de convidados
class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email