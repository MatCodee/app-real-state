from django.db import models

from django.db.models.signals import pre_save,post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver



def upload_location(instance, filename):
	file_path = 'Servicio{owner_id}/Bien{bienid}/{title}-{filename}'.format(
				owner_id=str(instance.owner.author.pk),bienid=str(instance.owner.title),title=str(instance.title), filename=filename)
	return file_path

    

def upload_location2(instance, filename):
	file_path = 'Servicio{owner_id}/Bien{bienow}/{title}-{filename}'.format(
				owner_id=str(instance.author.id),bienow=str(instance.title),title=str(instance.title), filename=filename)
	return file_path

# choices de la busqueda
REGION_STATUS = [
    (1,"Bio-Bio"),
    (2,"Metropolitana"),
]
OPERATION_STATUS = [
    (1,"Casas"),
    (2,"Departamentos"),
]
TYPE_STATUS = [
    (1,"Venta"),
    (2,"Arriendo"),
]

class BienRaiz(models.Model):
    title               = models.CharField(max_length=50, null=False, blank=False)
    description         = models.TextField(max_length=5000, null=False, blank=False)
    date_published      = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated        = models.DateTimeField(auto_now=True, verbose_name="date updated")
    price               = models.CharField(max_length=20,null=False, blank=False)                        # precio
    common_expenses     = models.IntegerField(null=True, blank=True)                                     # gastos comunes

    m2_construction         = models.IntegerField()                                     # metros cuadrados construccion
    m2_terrain              = models.IntegerField()                                     # metros cadrados terreno
    height                  = models.FloatField()                                       # alto
    width                   = models.FloatField()                                       # ancho
    n_bath                  = models.IntegerField()                                     # numero de baños
    n_room                  = models.IntegerField()                                     # numero habitaciones
    n_parking               = models.IntegerField()                                     # numero de estacionamiento
    n_flat                  = models.IntegerField()                                     # numero de pisos 
    country                 = models.CharField(max_length=50,null=False, blank=False)   # pais
    town                    = models.CharField(max_length=50,null=False, blank=False)   # ciudad
    sector                  = models.CharField(max_length=50,null=False, blank=False)   # sector
    
    is_vent                 = models.BooleanField()
    favorite                = models.BooleanField()

    # definicion de formulario de busqueda
    region                  = models.IntegerField(null=False, blank=False,choices=REGION_STATUS,default = 1)   # region
    operation               = models.IntegerField(null=False,blank=False,choices=OPERATION_STATUS,default = 1) 
    type_p                  = models.IntegerField(null=False,blank=False,choices=TYPE_STATUS,default = 1) 

    # definimos el usuario y el cosigo de servicio
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # usuario
    img_principal           = models.ImageField(upload_to=upload_location2, null=True, blank=True)
    
    
    # este es el codigo de busqueda de propiedad
    code                    = models.IntegerField(unique=True)
     


class galeryService(models.Model):
    title                   = models.CharField(max_length=50, null=False, blank=False)  
    image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True)
    owner 					= models.ForeignKey(BienRaiz, on_delete=models.CASCADE)
    slug                    = models.SlugField(blank=True, unique=True)




# esto esta bien definido(*)
@receiver(post_delete, sender=galeryService)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

def pre_save_service_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.owner.author.username + "-" + instance.title)

pre_save.connect(pre_save_service_receiver, sender=galeryService)