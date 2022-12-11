from django import forms 

# choices de la busqueda
REGION_STATUS = [
    (0,"Región"),
    (1,'Reg. Antofagasta'),
    (2,'Reg. Araucanía'),
    (3,'Reg. Bernardo OHiggins'),
    (4,'Reg. Bío-Bío'),
    (5,'Reg. Coquimbo'),
    (6,'Reg. Los Lagos'),
    (7,'Reg. Maule'),
    (8,'Reg. Metropolitana'),
    (9,'Reg. Ñuble'),
    (10,'Reg. Valparaiso'),
]
OPERATION_STATUS = [
    (0,"Tipo Propiedad"),
    (1,"Casa"),
    (2,"Departamento"),
    (3,"Oficina"),
    (4,"Sitio"),
    (5,"Local Comercial"),
    (6,"Industrial"),
    (7,"Agricola"),
    (8,"Parcela"),
    (9,"Terreno construccion"),
    (10,"Bodega"),
]

TYPE_STATUS = [
    (0,"Operación"),
    (1,"Venta"),
    (2,"Arriendo"),
]

class CreateBienForm(forms.Form):
    region = forms.ChoiceField(choices=REGION_STATUS,required = True)
    type_p = forms.ChoiceField(choices=OPERATION_STATUS,required = True)
    operation = forms.ChoiceField(choices=TYPE_STATUS,required = True)
    search = forms.CharField(label='Search', max_length=10)

