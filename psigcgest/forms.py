from django import forms
from django.forms import ModelForm, MultipleChoiceField, MultiValueField
#from bettersforms.multiforms import MultiModelForm
from psigcmod.models import Usuario, Noticia, Evento, Documento, AreaConocimiento,  Foro, ComentPost, EntidActor
from psigcmod.choices import cprovincias 
from psigcmod.forms import DateInput
#from psigcmod.forms import AreaConocForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo','contenido','entidactor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class':'form-control',})
        #self.fields['imagen'].widget.attrs.update({'class':'form-control',})
        self.fields['contenido'].widget.attrs.update({'class':'form-control',})
        self.fields['entidactor'].widget.attrs.update({'class':'form-control',})

class AreaConocForm(forms.ModelForm):
    #usuarios = forms.MultipleValueField(queryset=Usuario.objects.all(), label="Consultores y expertos en el tema")
    class Meta:
        model = AreaConocimiento
        fields = ['nombreareaconoc', 'descriparea','expertos',]
        widgets = {'expertos':forms.SelectMultiple(attrs={'class':'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombreareaconoc'].widget.attrs.update({'class':'form-control',})
        self.fields['descriparea'].widget.attrs.update({'class':'form-control',})
        self.fields['expertos'].widget.attrs.update({'class':'form-control',})
        
class EventoForm(forms.ModelForm):
    fechainicio = forms.DateField(widget=DateInput(), label = 'Fecha de inicio')
    fechafin = forms.DateField(widget=DateInput(), label = 'Fecha de finalizar')
    class Meta:
        model = Evento
        fields = ['titulo','fechainicio', 'fechafin', 'lugar','descrip','entidactor']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class':'form-control',})
        #self.fields['imagen'].widget.attrs.update({'class':'form-control',})
        self.fields['descrip'].widget.attrs.update({'class':'form-control',})
        self.fields['fechainicio'].widget.attrs.update({'class':'form-control','style':'widht: 50%'})
        self.fields['fechafin'].widget.attrs.update({'class':'form-control',})
        self.fields['entidactor'].widget.attrs.update({'class':'form-control',})

class DocumentoForm(forms.ModelForm):
    archivo = forms.FileField()
    class Meta:
        model = Documento
        fields = ['titulo','resegna','entidactor','archivo']
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class':'form-control',})
        #self.fields['imagen'].widget.attrs.update({'class':'form-control',})
        self.fields['archivo'].widget.attrs.update({'class':'form-control',})
        self.fields['resegna'].widget.attrs.update({'class':'form-control',})
        self.fields['entidactor'].widget.attrs.update({'class':'form-control',})

class ForoForm(forms.ModelForm):
    areacon = forms.ModelChoiceField(queryset=AreaConocimiento.objects.all(), label="Area del conocimiento")
    tema = forms.CharField(label="Formule la pregunta o tema a tratar")

    class Meta:
        model = Foro
        fields = ['areacon', 'tema', 'entidactor']

