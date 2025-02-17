from typing import Any, Dict
from django import forms
from django.forms import ModelForm, MultipleChoiceField, MultiValueField
#from bettersforms.multiforms import MultiModelForm
from .choices import coace, cprgdesarr
from .models import Usuario, Oace, ProgDesarrollo, EntidActor, InfoEjes, Provincia, Municipio
from django.contrib import messages
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type='date'

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name','last_name','username','genero','email','grdctfacad','municipio','is_staff','is_active','grupo','date_joined','princresult']
        exclude = ['last_login','user_permissions']

class OaceForm(forms.ModelForm):
    nombreoace = forms.ChoiceField(choices=coace, label='Nombre del Organismo de Administracion Central del Estao')
    #siglas = forms.ChoiceField(choices=coace, label='Nombre del Organismo de Administración Central del Estado')
    class Meta:
        model = Oace
        fields = ['nombreoace']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombreoace'].widget.attrs.update({'class':'form-control',})

class ProgDesaForm(forms.ModelForm):
    nombreprog = forms.ChoiceField(choices=cprgdesarr, label='Nombre del programa de desarrollo')

    class Meta:
        model = ProgDesarrollo
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.fields['nombreprog'].widget.attrs.update({'class':'form-control',})
        self.fields['descriprog'].widget.attrs.update({'class':'form-control',})
        self.fields['oacerector'].widget.attrs.update({'class':'form-control',})

class EntidActorForm(forms.ModelForm):
    class Meta:
        model = EntidActor
        fields = ['nombreactor','nombrecorto','tipoactor','pais','alcanc','prgdesarr','coordinador','altinfluenc', 'bajdepend','munic', 'oace']
    

class EjeInfoForm(forms.ModelForm):
    #provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(),  label='Provincia', widget=forms.Select(attrs={'class': 'form-control select2','autocomplete': 'on'}))
    fechaRegist = forms.DateField(widget=DateInput(), label = 'Fecha de registro')
    totalPers = forms.IntegerField(required=False)
    class Meta:
        model = InfoEjes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fechabase'].widget.attrs.update({'class':'form-control'})
        self.fields['entidactor'].widget.attrs.update({'class':'form-control form-control',})
        self.fields['fechaRegist'].widget.attrs.update({'class':'form-control datetimepicker',})
        self.fields['munic'].widget.attrs.update({'class':'form-control form-control',})
        self.fields['cantMujeres'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cant18_35'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cant36_55'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cant56_70'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cant_70'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantUniv'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantDrC'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantMSc'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantEsPost'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantTNS'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantTM'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantOb'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantOC'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantEspCap'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantPrdCap'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantCuadCap'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantResCuad'].widget.attrs.update({'class':'form-control form-control-sm',})

        self.fields['cantCTA'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantIP_CTA'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantIA_CTA'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantECTI'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantPECTIC'].widget.attrs.update({'class':'form-control form-control-sm',})

        self.fields['cantPAP'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantPNAP'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantPCI'].widget.attrs.update({'class':'form-control form-control-sm',}) 
        self.fields['cantPDL'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantPSP'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['finanPAP'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['finanPNAP'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['finanPCI'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['finanPDL'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['finanPSP'].widget.attrs.update({'class':'form-control form-control-sm',})

        self.fields['cantRCLA'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantILA'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantTec'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantProc'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantProd'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantRDExt'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantRRS'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantRING'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantAccExt'].widget.attrs.update({'class':'form-control form-control-sm',})
        self.fields['cantPDiv'].widget.attrs.update({'class':'form-control form-control-sm',})
    
    def clean(self):
        super(EjeInfoForm, self).clean()
        fbase = False
        fechab = ''
        ufecha=''
        if self.cleaned_data.get('entidactor') and self.cleaned_data.get('munic'):
            regdatos = InfoEjes.objects.filter(entidactor=self.cleaned_data.get('entidactor'), munic=self.cleaned_data.get('munic')).order_by('fechaRegist')
            if len(regdatos) >= 1:
                for dato in regdatos:
                    if dato.fechabase:
                        fbase = True
                        fechab = dato.fechaRegist
                    ufecha = dato.fechaRegist
                if self.cleaned_data.get('fechabase'):
                    if fbase and fechab != self.cleaned_data.get('fechaRegist'):
                        self._errors['Fecha base'] = self.error_class(['Ya existe un registro como fecha base para esta Entidad-Actor y municipio'])
                    if not fbase and ufecha <= self.cleaned_data.get('fechaRegist'):
                        self._errors['Fecha base'] = self.error_class(['La fecha elegida no puede ser fecha base porque existen registros anteriores a la fecha elegida'])
            
            regdatos = EntidActor.objects.filter(nombreactor=self.cleaned_data.get('entidactor'))
            if len(regdatos) > 0:
                for dato in regdatos:
                    if dato.alcanc == 'Municipal' and self.cleaned_data.get('munic') != dato.munic:
                        self._errors['Alcance de la Entidad-Actor(municipal)'] = self.error_class(['El municipio elegido de aplicación del SIGC debe ser el mismo al que pertenece la Entidad-Actor'])

                    muniprov = Municipio.objects.filter(prov=dato.munic.prov)
                    if  dato.alcanc == 'Provincial' and not self.cleaned_data.get('munic') in muniprov:
                        self._errors['Alcance de la Entidad-Actor(provincial)'] = self.error_class(['El municipio elegido de aplicación del SIGC no pertenece a la misma provincia de la Entidad-Actor'])


        grpedades = self.cleaned_data.get('cant18_35') + self.cleaned_data.get('cant36_55') + self.cleaned_data.get('cant56_70') + self.cleaned_data.get('cant_70')

        formacion = self.cleaned_data.get('cantUniv') + self.cleaned_data.get('cantTNS') + self.cleaned_data.get('cantTM') + self.cleaned_data.get('cantOb')

        if grpedades != formacion:
            self._errors['Grupo de edades'] = self.error_class(['La suma de personas en grupos de edades debe coincidir con el total de personas en formación' ])

        feminas = self.cleaned_data.get('cantMujeres')
        if feminas > grpedades or feminas > formacion:
            self._errors['Féminas'] = self.error_class(['La cantidad de mujeres debe ser menor o igual al total de personas en grupos de edades o en formación' ])

        if formacion != grpedades:
            self._errors['Formación'] = self.error_class(['La suma de personas en Formación debe ser igual al total en grupo de edades' ])

        superacion = self.cleaned_data.get('cantDrC') + self.cleaned_data.get('cantMSc') + self.cleaned_data.get('cantEsPost')
        if superacion > self.cleaned_data.get('cantUniv'):
            self._errors['Superación'] = self.error_class(['La suma de personas en Superación debe ser menor o igual al total de universitarios' ])

        capacitacion = self.cleaned_data.get('cantOC') + self.cleaned_data.get('cantEspCap') + self.cleaned_data.get('cantPrdCap') + self.cleaned_data.get('cantCuadCap') + self.cleaned_data.get('cantResCuad')
        if capacitacion > grpedades or capacitacion > grpedades:
            self._errors['Capacitación'] = self.error_class(['La suma de personas en Capacitación debe ser menor o igual al total de personas (grupos de edades o fomación)' ])

        dirigentes = self.cleaned_data.get('cantCuadCap') + self.cleaned_data.get('cantResCuad') 
        if dirigentes > self.cleaned_data.get('cantUniv') + self.cleaned_data.get('cantTNS'):
            self._errors['Capacitación'] = self.error_class(['La suma de cuadros capacitados y reservas de cuadros capacitados no debe se mayor a la cantidad de universitarios' ])
        
        especialistas = self.cleaned_data.get('cantUniv') + self.cleaned_data.get('cantTNS') 
        if self.cleaned_data.get('cantEspCap') > especialistas:
            self._errors['Capacitación'] = self.error_class(['La cantidad de especialistas capacitados no debe ser mayor a la suma de universitarios y técnicos de nivel superior' ])

        if self.cleaned_data.get('cantPECTIC') > grpedades or self.cleaned_data.get('cantPECTIC') > grpedades:
            self._errors['Personas atienden CTI'] = self.error_class(['La cantidad de personas que atienden la actividad de CTI no debe ser mayor al total de personas' ])

        if self.cleaned_data.get('cantIP_CTA') < self.cleaned_data.get('cantIA_CTA'):
            self._errors['Innovaciones presentadas a CTAs'] = self.error_class(['La cantidad de la cantidad de innovaciones propuestas no puede ser mayor que las aprobadas' ])

        if self.cleaned_data.get('cantPDiv') > grpedades or self.cleaned_data.get('cantPDiv') > grpedades:
            self._errors['Personas atienden extensionismo'] = self.error_class(['La cantidad de personas vinculadas a la divulgación/extensionismo no debe ser mayor al total de personas' ])

        if self.cleaned_data.get('cantPAP') == 0 and  self.cleaned_data.get('finanPAP') != 0:
            self._errors['Proyectos y financiamiento de PAP'] = self.error_class(['No debe existir financiamiento si no es a partir de proyectos' ])

        if self.cleaned_data.get('cantPNAP') == 0 and  self.cleaned_data.get('finanPNAP') != 0:
            self._errors['Proyectos y financiamiento de PNAP'] = self.error_class(['No debe existir financiamiento si no es a partir de proyectos' ])

        if self.cleaned_data.get('cantPCI') == 0 and  self.cleaned_data.get('finanPCI') != 0:
            self._errors['Proyectos y financiamiento de PCI'] = self.error_class(['No debe existir financiamiento si no es a partir de proyectos' ])

        if self.cleaned_data.get('cantPDL') == 0 and  self.cleaned_data.get('finanPDL') != 0:
            self._errors['Proyectos y financiamiento de PDL'] = self.error_class(['No debe existir financiamiento si no es a partir de proyectos' ])

        if self.cleaned_data.get('cantPSP') == 0 and  self.cleaned_data.get('finanPSP') != 0:
            self._errors['Proyectos y financiamiento de PSP'] = self.error_class(['No debe existir financiamiento si no es a partir de proyectos' ])

        return self.cleaned_data