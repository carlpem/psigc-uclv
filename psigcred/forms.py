from django import forms
from django.forms import ModelForm, MultipleChoiceField, MultiValueField
#from bettersforms.multiforms import MultiModelForm
from psigcmod.models import Usuario, DemandaBD, Noticia, ComentPost, ComentReply
from psigcmod.choices import cprovincias


class DemandaForm(forms.ModelForm):
    expertos = forms.ModelChoiceField(queryset=Usuario.objects.all(), label="Elija un consultor o experto ")

    class Meta:
        model = DemandaBD
        fields = ['tipodemand','areaconoc', 'expertos','descripcion']

class PostForm(forms.ModelForm):

    class Meta:
        model = Noticia
        fields = '__all__'

class ComentForm(forms.ModelForm):
    comentcont = forms.CharField(widget=forms.Textarea(attrs={'class':'shadow-sm focus-ring-indigo-400', 'rows':'3', 'placeholder':'Escriba su respuesta o intervención aqui'}), label='',required=True)
    
    class Meta:
        model = ComentPost
        fields = ['comentcont']


class ReplyComentForm(forms.ModelForm):
    replycont = forms.CharField(widget=forms.Textarea(attrs={'class':'shadow-sm focus-ring-indigo-300', 'rows':'1', 'placeholder':'Comente esta intervención'}), label='',required=True)
    
    class Meta:
        model = ComentReply
        fields = ['replycont']