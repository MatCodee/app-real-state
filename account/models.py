from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

from django.db.models.signals import pre_save,post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver



def upload_location(instance, filename):
	file_path = 'user{user_id}/{username}-{filename}'.format(
				user_id=str(instance.id),username=str(instance.username), filename=filename)
	return file_path

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password = None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
                email = self.normalize_email(email),
                username = username,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):        
        user = self.create_user(
                email = self.normalize_email(email),
                username = username,
                password =password,
                
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user



# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email",max_length=60,unique=True)
    username = models.CharField(max_length=30,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add = True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now = True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)

    # campos de usuario de la pagina
    image_owner = models.ImageField(upload_to=upload_location, null=True, blank=True)
    phone = models.CharField(max_length=20)
    contacted = models.BooleanField(default=False)
    location = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    slug = models.SlugField(blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username",]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # funciones para un usuario personalizado
    def has_perm(self,perm,obj = None):
        return self.is_admin 

    def has_module_perms(self,app_label):
        return True
    


# esto esta bien definido(*)
@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

def pre_save_account_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.username + "-" + str(instance.id))

pre_save.connect(pre_save_account_receiver, sender=Account)