# ----------------------------------------------------------
# Django - Personalizar Authentication con clases abstractas
# ----------------------------------------------------------

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Esta clase extiende en Django y proporciona métodos para la creación de usuarios regulares y superusuarios.
class MyAccountManager(BaseUserManager):
    
    # La creacion de un USUARIO REGULAR, que no tiene permisos de super user:
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('el usuario debe tener un email')

        if not username:
            raise ValueError('el usuario debe tener un username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Usuario SuperAdmin:
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password=password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# Cleando clase Cuenta representa un modelo de usuario personalizado que hereda de AbstractBaseUser, que es una clase abstracta provista por Django para personalizar el modelo de usuario predeterminado.
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #campos atributos de django
    date_joined = models.DateTimeField(auto_now_add=True) # La fecha que se esta agregando este usuario.
    last_login = models.DateTimeField(auto_now_add=True) # la ultima que se a logeado.add()
    is_admin = models.BooleanField(default=False) # si es administrador o no.
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager() # Con esta INSTANCIA ya voy a poder instanciar los métodos create_user y create_superuser.

    # creando funciones de soporte:
    def full_name(self):
        return f'{self.first_name} {self.last_name}' # devuelva su nombre completo.
    
    def __str__(self):
        return self.email # Para ver los usuarios registrados con su email.
    
    def has_perm(self, perm, obj=None):
        return self.is_admin # para ver si tiene permisos.
    
    def has_module_perms(self, add_label): # si es True los permisos ADMIN (Esta funcion trabaja juntas con el 'has_perm')
        return True
    























