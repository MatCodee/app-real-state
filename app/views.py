from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import templatize

from service.models import BienRaiz,galeryService

from django.db.models import Q
from operator import attrgetter
from service.forms import CreateBienForm


'''
# esta funcion va a hacer el query
def get_bienRaiz_queryset(query=None):
	queryset = []    
	queries = query 

	posts = BienRaiz.objects.filter(Q(region=queries[1]) & Q(type_p=queries[2]) & Q(operation=queries[3]) 
        ).distinct()

	for post in posts:
		queryset.append(post)

	return list(set(queryset))
'''

# aqui vamos a implementar le query
def home_page(request):
    context = {}
    form = CreateBienForm()  
    if request.GET:
        form = CreateBienForm(request.GET)       
        if form.is_valid():
            if int(form.cleaned_data['region']) == 0 and int(form.cleaned_data['type_p']) == 0 and int(form.cleaned_data['operation']) ==0:
                bien_raiz = BienRaiz.objects.all()
            elif form.cleaned_data['search']:
                bien_raiz = BienRaiz.objects.get(code=form.cleaned_data['search'])
            else:
                bien_raiz = BienRaiz.objects.all().filter(
                    region=form.cleaned_data['region'],
                    type_p=form.cleaned_data['type_p'],
                    operation=form.cleaned_data['operation']
                )
            context['servicios'] = bien_raiz

        context['form'] = form
        return render(request,'search.html',context)
    
    bien_raiz = BienRaiz.objects.all()

    context['form'] = form    
    context['servicios'] = bien_raiz
    return render(request,'home.html',context)



def nosotros_page(request):
    return render(request,'nosotros.html',{})

def servicios_page(request):
    return render(request,'servicios.html',{})


from .forms import CreateClientForm
from django.core.mail import send_mail,BadHeaderError,EmailMultiAlternatives
from decouple import config
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
# este es el campo del formulario

def contacto_page(request):
    form = CreateClientForm()
    context = {}

    if request.method == 'POST':
        form = CreateClientForm(request.POST)
        if form.is_valid():
            form.save()
            
            config_email_destino = config('USER_MAIL_USER_DES')
            send_email_function(config_email_destino,form)

    context['form'] = form
    return render(request,'contacto.html',{'form':form})



def venta_page(request):
    context = {} 
    servicio = BienRaiz.objects.filter(is_vent = True,)
    context['servicios'] = servicio
    return render(request,'venta.html',context)

def arriendo_page(request):
    context = {} 
    servicio = BienRaiz.objects.filter(is_vent = False)
    context['servicios'] = servicio
    return render(request,'arriendo.html',context)


# configuracion de envio de correo en la pagina de la empresa




def send_email_function(mail,cliente):
    info_form = cliente.cleaned_data
    lista_Datos = [info_form['name'],info_form['phone'],info_form['email'],info_form['message']]  

    context = {'email':mail,'cliente':info_form}

    template = get_template('send/send.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'un correo de prueba',
        'Empresa',
        settings.EMAIL_HOST_USER,
        [mail],
    )
    email.attach_alternative(content,'text/html')
    email.send()



def detail_service(request,id):

    context = {}
    services = BienRaiz.objects.get(id=id)
    gal = galeryService.objects.filter(owner=services)

    if len(gal) == 1 or len(gal) == 0:
        context["primera_imagen"] = gal
    else:
        context['primera_imagen'] = gal[0]
        context["servicio_imagen"] = gal[1:]
    context["servicios"] = services
    
    return render(request,'detail.html',context)

from django.views.generic import TemplateView
class TestVie(TemplateView):
    template_name = 'test.html'
    
