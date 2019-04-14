from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(email=self.normalize_email(email),name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, password):
        user = self.create_user(email,password=password,name=name)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    image = models.ImageField(default="profile/default.jpg", upload_to="profile/")
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)
    name = models.CharField(max_length=150)
    github_name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name',]

    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
    
    @property
    def printer(self):
        return "Apple"

class Github_model(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    url = models.CharField(max_length=800)
    discription = models.TextField()
    languages = models.CharField(max_length=800)
    created_at = models.DateField()
    stars = models.IntegerField()

    def __str__(self):
        return self.name