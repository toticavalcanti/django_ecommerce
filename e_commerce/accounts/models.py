from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):

    def create_user(self, email, full_name = None, password = None, is_active = True, is_staff = False, is_admin = False):
        if not email:
            raise ValueError("O Usuário deve ter um endereço de email!")
        if not password:
            raise ValueError("O Usuário deve ter uma senha!")
        user_obj = self.model(
            full_name = full_name,
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) # muda a senha
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj
    def create_staffuser(self, email, full_name = None, password = None):
        user = self.create_user(
            email,
            full_name,
            password = password,
            staff = True
        )
        return user
    def create_superuser(self, email, full_name = None, password = None):
        user = self.create_user(
            email,
            full_name = full_name,
            password = password,
            is_staff = True,
            is_admin = True,
        )

class User(AbstractBaseUser):
    full_name  = models.CharField(max_length=255, blank=True, null=True)
    email       = models.EmailField(max_length=255, unique=True)
    active      = models.BooleanField(default=True) # can do login
    staff       = models.BooleanField(default=False) # staff user, non superuser
    admin       = models.BooleanField(default=False) #superuser
    timestamp    = models.DateTimeField(auto_now_add=True)
    # confirm    = models.BooleanField(default=False)
    # confirmed_date    = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] # ['full_name'] #python manage.py createsuperuser
    objects = UserManager()

    def __str__(self):
        return self.email
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email
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

class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email