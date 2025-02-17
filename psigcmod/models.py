from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from .choices import ctipodemand, cgenero, cgrd, ctiporg, cpais, cgrp, calcanc, cpublic
from django.core.exceptions import ValidationError

# Create your models here.

class Provincia(models.Model):
    idprov = models.AutoField(primary_key=True)
    nombreprov = models.CharField(max_length=100, unique=True)
    siglas = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self) :
        return self.nombreprov
    
    class Meta:
        verbose_name ='Provincia'
        verbose_name_plural='Provincias'
        db_table ='provincia'
     
class Municipio(models.Model):
    idmun = models.AutoField(primary_key=True)
    nombremun = models.CharField(max_length = 100, unique=True)
    prov = models.ForeignKey("Provincia", on_delete=models.CASCADE)

    class Meta:
        verbose_name ='Municipio'
        verbose_name_plural ='Municipios'
        db_table ='municipio'

    def __str__(self) :
        return self.nombremun

class Procedencia(models.Model):
    provincia = models.OneToOneField("Provincia", on_delete=models.CASCADE, verbose_name='Provincia de procedencia*')
    municipio = models.OneToOneField("Municipio", on_delete=models.CASCADE, verbose_name='Municipio de procedencia*')

class ContactoBD(models.Model):
    idcontact = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 100, verbose_name="Nombre(s) y apellidos*")
    municipio = models.ForeignKey("Municipio", on_delete=models.SET_NULL, verbose_name='Municipio de procedencia', null=True, blank=True)
    ecorreo = models.EmailField(max_length = 100, verbose_name="Correo electrónico*")
    asunto = models.CharField(max_length = 200, verbose_name="Tema a tratar ")
    contenido = models.TextField(verbose_name="Contenido del mensaje")
    respuesta = models.TextField(verbose_name="Respuesta", null=True, blank=True)
    fechaenvio = models.DateField(auto_now_add=True,)

    class Meta:
        verbose_name ='Contactos enviado'
        verbose_name_plural='Contactos enviados'
        ordering = ['-fechaenvio']   
        db_table ='contacto'
    
    def __str__(self):
        return self.fechaenvio + " - " + self.nombre

class Grupo(Group):
    nombregrupo = models.CharField(max_length=20, choices=cgrp, verbose_name="Grupo de usuario", default='Invitados')
    class Meta:
        verbose_name= 'Grupo'
    def __str__(self):
        self = self.nombregrupo
        return self

class Usuario(AbstractUser):
    ingreso = models.DateField(auto_now_add=True,)
    municipio=models.ForeignKey("Municipio", on_delete=models.SET_NULL, verbose_name="Municipio de procedencia", blank=True, null=True)
    genero = models.CharField(max_length = 10, verbose_name="Género", choices=cgenero, null=True, default='')
    grdctfacad = models.CharField(max_length=20, choices=cgrd, verbose_name="Último título académico o científico alcanzado",blank=True, null=True)
    princresult = models.TextField(verbose_name="Principales resultados científicos", blank=True, null=True)
    foto=models.ImageField(default='', upload_to='Profiles/', null=True, blank=True)
    grupo = models.ForeignKey("Grupo", verbose_name='Grupo de usuarios', on_delete=models.SET_NULL, null=True, blank=True)

    #activation_key = models.CharField(max_length=40, blank=True)
    #key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        self = self.last_name + " " + self.first_name + " (" + self.username + ")"
        return self

    class Meta: 
        verbose_name = 'Usuario'
        ordering = ['last_name', 'first_name',]
        db_table = 'usuario'

class AreaConocimiento(models.Model):
    idareaconoc = models.AutoField(primary_key=True)
    nombreareaconoc = models.CharField(max_length=100,verbose_name="Nombre del área ")
    descriparea= models.TextField(verbose_name="Descripción del tema ", null=True, blank=True, default='Descripción aún sin especificar')
    expertos = models.ManyToManyField("Usuario", verbose_name="Experto(s) en el tema", blank=True)

    class Meta:
        verbose_name = 'Área de conocimiento'
        verbose_name_plural = 'Áreas de conocimiento' 
        ordering = ['nombreareaconoc']   
        db_table ='areaconoc'
    
    def __str__(self) :
        return self.nombreareaconoc

class Oace(models.Model):
    idoace = models.AutoField(primary_key=True)
    siglas = models.CharField(max_length=10, verbose_name="Siglas", unique=True)
    nombreoace = models.CharField(max_length=60, verbose_name="Nombre del Organismo de Administración Central del Estado", unique=True)

    class Meta:
        verbose_name = 'Organismo del Estado'
        verbose_name_plural = 'Organismos del Estado' 
        ordering = ['nombreoace']   
        db_table ='oace'

    def __str__(self) :
        return self.nombreoace
    
    def save(self, *args, **kwargs):
        if  self.nombreoace == 'Ministerio de Ciencia, Tecnología y Medio Ambiente':
            self.siglas = 'CITMA'
        elif self.nombreoace == 'Ministerio del Comercio exterior e Inversión extranjera':
            self.siglas = 'MINCEX'
        elif self.nombreoace == 'Ministerio del Comercio Interior':
            self.siglas = 'MINCIN'
        elif self.nombreoace == 'Ministerio de Comunicaciones':
            self.siglas = 'MINCOM'
        elif self.nombreoace == 'Ministerio de Cultura':
            self.siglas = 'MINCULT'
        elif self.nombreoace == 'Ministerio de Educación':
            self.siglas = 'MINED'
        elif self.nombreoace == 'Ministerio de Educación Superior':
            self.siglas ='MES'
        elif self.nombreoace == 'Ministerio de Energía y Minas':
            self.siglas ='MINER'
        elif self.nombreoace == 'Ministerio de Finanzas y Precios':
            self.siglas = 'MFP'
        elif self.nombreoace == 'Ministerio de Industria Alimentaria':
            self.siglas = 'MINAL'
        elif self.nombreoace == 'Ministerio de Industrias':
            self.siglas = 'MINBAS'
        elif self.nombreoace == 'Ministerio de Justicia':
            self.siglas ='MINJUS'
        elif self.nombreoace == 'Ministerio de la Agricultura':
            self.siglas ='MINAG'
        elif self.nombreoace == 'Ministerio de la Construcción':
            self.siglas = 'MICONS'
        elif self.nombreoace == 'Ministerio de las Fuerzas Armadas':
            self.siglas = 'MINFAR'
        elif self.nombreoace == 'Ministerio de Relaciones Exteriores':
            self.siglas = 'MINREX'
        elif self.nombreoace == 'Ministerio de Salud Publica':
            self.siglas ='MINSAP'
        elif self.nombreoace == 'Ministerio de Transporte':
            self.siglas ='MITRANS'
        elif self.nombreoace == 'Ministerio de Turismo':
            self.siglas = 'MINTUR'
        elif self.nombreoace == 'Ministerio del Interior':
            self.siglas = 'MININT'
        elif self.nombreoace == 'Tribunal Supremo Popular':
            self.siglas = 'TSP'
        elif self.nombreoace == 'Banco Central de Cuba':
            self.siglas = 'BCC'
        elif self.nombreoace == 'Contraloría General de la República':
            self.siglas = 'CGR'
        elif self.nombreoace == 'Fiscalía General de la República':
            self.siglas = 'FGR'
        elif self.nombreoace == 'Instituto de Información y Comunicación Social':
            self.siglas = 'IICS'
        elif self.nombreoace == 'Instituto Nacional de Recursos Hidráulicos':
            self.siglas = 'INRH'
        elif self.nombreoace == 'Instituto Nacional de Deporte y Recreación':
            self.siglas ='INDER'
        elif self.nombreoace == 'Asamblea del Poder Popular (Gobierno)':
             self.siglas = 'APP'
        super(Oace, self).save(*args, **kwargs)

class ProgDesarrollo(models.Model):
    idprog = models.AutoField(primary_key=True)
    nombreprog = models.CharField(max_length=100, verbose_name="Nombre del programa de desarrollo", unique=True)
    descriprog = models.TextField(default="Descripción aún sin especificar", verbose_name="Descripción del programa", null=True, blank=True)
    oacerector = models.ForeignKey("Oace", verbose_name="Organismo rector",on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Programa de desarrollo'
        verbose_name_plural = 'Programas de desarrollo' 
        ordering = ['nombreprog']   
        db_table ='progdesarrollo'
    
    def __str__(self) :
        return self.nombreprog

class EntidActor(models.Model):
    idactor = models.AutoField(primary_key=True)
    nombreactor = models.CharField(max_length=100, verbose_name="Nombre de Entidad-Organización-Actor", null=False, blank=False, unique=True)
    nombrecorto = models.CharField(max_length=20, verbose_name="Nombre corto o Siglas de Entidad-Actor", unique=True)
    tipoactor = models.CharField(max_length=3, choices=ctiporg, null=False, default='GUB')
    pais = models.CharField(max_length=100, choices=cpais, verbose_name="País procedencia de la entidad")
    alcanc = models.CharField(max_length=10, choices=calcanc, verbose_name="Alcance del SIGC", null=False, default='Municipal')
    prgdesarr = models.ManyToManyField("ProgDesarrollo", verbose_name ="Programa(s) de desarrollo que ejecuta", related_name="programas")
    coordinador = models.ForeignKey("Usuario", verbose_name="Coordinador o representante principal", on_delete=models.SET_NULL, null=True, blank=True)
    altinfluenc = models.BooleanField(default=False, verbose_name="Alta Influencia")
    bajdepend = models.BooleanField(default=False, verbose_name="Baja dependencia")    
    munic = models.ForeignKey("Municipio", verbose_name="Municipio de la Entidad-Actor", on_delete=models.CASCADE, null=True, blank=True)
    oace = models.ForeignKey("Oace", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Organismo Administración Central Estado al que pertenece (entidad nacional)")
    
    class Meta:
        verbose_name = 'Entidad_Actor'
        verbose_name_plural = 'Entidad_Actores' 
        ordering = ['nombreactor']   
        db_table ='entidactor'

    def __str__(self) :
        return self.nombreactor

class InfoEjes(models.Model):
    idinfo = models.AutoField(primary_key=True)
    fechaRegist = models.DateField(auto_now_add=False, verbose_name='Fecha del registro')
    fechabase = models.BooleanField(verbose_name='Fecha base', default=False)
    entidactor = models.ForeignKey("EntidActor", on_delete=models.CASCADE, related_name='entidactores', verbose_name='Entidad-Actor')
    munic = models.ForeignKey("Municipio", on_delete=models.CASCADE, related_name='municipios', verbose_name='Municipio SIGC')

    class Meta: 
        unique_together = ['fechaRegist','entidactor','munic']
        verbose_name = 'Información de los ejes'
        ordering = ['-fechaRegist','entidactor','munic']
        db_table = 'infoejes'

    def __str__(self):
        self = str(self.fechaRegist) + " " + self.entidactor.nombrecorto
        return self

    # Recurso Formación, Superación, Capacitación
    
    totalPers = models.PositiveSmallIntegerField(default=0,verbose_name='Total de Personas', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.totalPers = self.cantUniv + self.cantTNS + self.cantTM + self.cantOb
        super(InfoEjes, self).save(*args, **kwargs)
   
    cantMujeres = models.PositiveSmallIntegerField(default=0,verbose_name='Féminas')
    cant18_35 = models.PositiveSmallIntegerField(default=0,verbose_name='Edades 18-35')
    cant36_55 = models.PositiveSmallIntegerField(default=0,verbose_name='Edades 36-55')
    cant56_70 = models.PositiveSmallIntegerField(default=0,verbose_name='Edades 56-70')
    cant_70 = models.PositiveSmallIntegerField(default=0,verbose_name='Edades +70')
    cantUniv = models.PositiveSmallIntegerField(default=0,verbose_name='Universitarios')
    cantDrC = models.PositiveSmallIntegerField(default=0,verbose_name='Doctores en Ciencias')
    cantMSc = models.PositiveSmallIntegerField(default=0,verbose_name='Masters en Ciencias.')
    cantEsPost = models.PositiveSmallIntegerField(default=0,verbose_name='Especialidad de Postgrado')
    cantTNS = models.PositiveSmallIntegerField(default=0,verbose_name='Técnicos Nivel Superior')
    cantTM = models.PositiveSmallIntegerField(default=0,verbose_name='Técnicos Nivel Medio')
    cantOb = models.PositiveSmallIntegerField(default=0,verbose_name='Obreros (Escuela de oficio)')
    cantOC = models.PositiveSmallIntegerField(default=0,verbose_name='Obreros capacitados')
    cantEspCap = models.PositiveSmallIntegerField(default=0,verbose_name='Especialistas capacitados')
    cantPrdCap = models.PositiveSmallIntegerField(default=0,verbose_name='Productores capacitados')
    cantCuadCap = models.PositiveSmallIntegerField(default=0,verbose_name='Cuadros capacitados')
    cantResCuad = models.PositiveSmallIntegerField(default=0,verbose_name='Reservas cuadros capacitados')
           
    #Recurso Organización
    cantCTA = models.PositiveSmallIntegerField (default=0,verbose_name='CTAs-dedicados al programa')
    cantIP_CTA = models.PositiveSmallIntegerField (default=0,verbose_name='Innovaciones propuestas a CTAs')
    cantIA_CTA = models.PositiveSmallIntegerField (default=0,verbose_name='Innovaciones avaladas por CTAs')
    cantECTI = models.PositiveSmallIntegerField (default=0,verbose_name='Nuevas ECTIs')
    cantPECTIC = models.PositiveSmallIntegerField (default=0,verbose_name='Personas atienden ETICs y/o CTAs')

    #Recurso Proyecto
    cantPAP = models.PositiveSmallIntegerField (default=0,verbose_name='Proyectos Asociados a Programa')
    cantPNAP = models.PositiveSmallIntegerField (default=0,verbose_name='Proyectos no Asociados a Programa')
    cantPCI = models.PositiveSmallIntegerField (default=0,verbose_name='Proyectos con Cooperacion Internacional')
    cantPDL = models.PositiveSmallIntegerField (default=0,verbose_name='Proyectos de Desarrollo Local')
    cantPSP = models.PositiveSmallIntegerField (default=0,verbose_name='Proyectos del Sector Productivo')

    finanPAP = models.FloatField (default=0,verbose_name='Financiamiento a PNAP')
    finanPNAP = models.FloatField (default=0,verbose_name='Financiamiento a PAP')
    finanPCI = models.FloatField (default=0,verbose_name='Financiamiento a PCI')
    finanPDL = models.FloatField (default=0,verbose_name='Financiamiento a PDL')
    finanPSP = models.FloatField (default=0,verbose_name='Financiamiento a PSP')
    
    #Recurso Extensión
    cantRCLA = models.PositiveSmallIntegerField (default=0,verbose_name='Resultados introducidos')
    cantILA = models.PositiveSmallIntegerField (default=0,verbose_name='Innovaciones introducidas')
    cantTec = models.PositiveSmallIntegerField (default=0,verbose_name='Tecnologías generadas')
    cantProc = models.PositiveSmallIntegerField (default=0,verbose_name='Procesos generados')
    cantProd = models.PositiveSmallIntegerField (default=0,verbose_name='Producciones generadas')
    cantRDExt = models.PositiveSmallIntegerField (default=0,verbose_name='Resultados divulgados extensionista')
    cantRRS = models.PositiveSmallIntegerField (default=0,verbose_name='Resultados en libros,revistas,redes sociales')
    cantAccExt = models.PositiveSmallIntegerField (default=0,verbose_name='Acciones extensionistas')
    cantRING = models.PositiveSmallIntegerField (default=0,verbose_name='Redes grupos y nodos de innovación')
    cantPDiv = models.PositiveSmallIntegerField (default=0,verbose_name='Personas vinculadas a divulgación/extensionismo')

class DemandaBD(models.Model):
    iddemanda = models.AutoField(primary_key=True)
    entidactor = models.ForeignKey("EntidActor", on_delete=models.CASCADE, verbose_name="Entidad-Actor")
    areaconoc = models.ForeignKey("AreaConocimiento", on_delete=models.DO_NOTHING, verbose_name="Área del conocimiento")
    tipodemand = models.CharField(max_length = 10, choices=ctipodemand, verbose_name="Categoría o tipo de demanda")
    descripcion = models.TextField(default='Describa la(s) necesidad(es) y posibles propuesta de soluciones', verbose_name="Descripción de la demanda")
    respuesta = models.TextField(verbose_name="Respuesta o solución a la demanda", null=True, blank=True)
    usuario = models.ForeignKey("Usuario", on_delete=models.DO_NOTHING, null=True, blank=True)
    fechasolic = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name ='Demanda solicitada'
        verbose_name_plural='Demandas solicitadas'
        db_table ='demandabd'

class Publicacion(models.Model):
    titulo = models.CharField(max_length=100, unique=True, null=False, verbose_name='Título')
    autor = models.ForeignKey("Usuario", on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to="Publicacion", null=True, blank=True)
    entidactor = models.ForeignKey("EntidActor", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Entidad-Actor que publica")
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tipopub = models.CharField(max_length=9, choices=cpublic, null=False, default='Noticia')
       
    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'
        ordering = ['-creado']
        db_table = 'publicacion'

    def __str__(self):
        lentitle = 15
        if len(self.titulo) > lentitle:
            self= self.titulo[:lentitle] + "..."
        else:
            return self.titulo  
        return self

class Noticia(Publicacion):
    idpost = models.AutoField(primary_key=True)
    contenido = models.TextField(default='', null=True, verbose_name='Contenido de la publicación')
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-creado']
        db_table = 'noticia'

class Evento(Publicacion):
    idevento = models.AutoField(primary_key=True)
    lugar = models.CharField(default="Aún por definir...", max_length=50, verbose_name="Lugar")
    descrip = models.TextField(default='Esté atento a este evento, próximo a celebrarse', null=True, verbose_name='Descripción')
    fechainicio = models.DateTimeField(null=True, blank=True, default='')
    fechafin = models.DateTimeField(null=True, blank=True, default='')

    class Meta:
        verbose_name = 'Evento'
        ordering = ['fechainicio']
        db_table = 'evento'
        
class Documento(Publicacion):
    iddoc = models.AutoField(primary_key=True)
    resegna = models.CharField(verbose_name='Reseña del contenido',max_length=200)
    archivo = models.FileField(upload_to='Archivos/', verbose_name='Documento a subir')
    
    class Meta:
        verbose_name = 'Documento'
        db_table = 'documento'

class Foro(models.Model):
    idforo = models.AutoField(primary_key=True)
    areacon = models.OneToOneField("AreaConocimiento", on_delete=models.CASCADE, verbose_name="Área del conocimiento")
    tema = models.CharField(verbose_name='Tema o pregunta de debate',max_length=500)
    moderador = models.ForeignKey("Usuario", on_delete=models.SET_NULL, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    entidactor = models.ForeignKey("EntidActor", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Entidad-Actor que publica")
    likes = models.ManyToManyField("Usuario", related_name='likes',verbose_name="Me gusta")
    dlikes = models.ManyToManyField("Usuario", related_name='dlikes',verbose_name="Me gusta")

    class Meta:
        verbose_name = 'Foro'
        db_table = 'foro'
    
    def __str__(self):
        return self.areacon.nombreareaconoc

opcestado = [('Pendiente','Pendiente'),('Aceptado','Aceptado'),('Rechazado','Rechazado')]

class ComentPost(models.Model):
    idcoment = models.AutoField(primary_key=True)
    forodebate = models.ForeignKey("Foro", on_delete=models.CASCADE, related_name='comentarios')
    comentautor = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    comentcont = models.TextField(verbose_name='Comentario')
    postdate = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(default='Pendiente',max_length=10, choices=opcestado)

    class Meta:
        verbose_name = 'Comentario'
        ordering = ['-postdate']
        db_table = 'comentpost'
    
    def __str__(self):
        lencoment = 30
        if len(self.comentcont) > lencoment:
            return '('+ self.comentautor.username + ') ' + self.comentcont[:lencoment] + '...'
        else:
            return '('+ self.comentautor.username + ') ' + self.comentcont    

class ComentReply(models.Model):
    idrepl = models.AutoField(primary_key=True)
    comentforo = models.ForeignKey("ComentPost", on_delete=models.CASCADE, related_name='respuestas')
    replyautor = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    replycont = models.TextField(verbose_name='Respuesta')
    replydate = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(default='Pendiente',max_length=10, choices=opcestado)

    class Meta:
        verbose_name = 'Respuesta'
        ordering = ['-replydate']
        db_table = 'replypost'
    
    def __str__(self):
        lencoment = 30
        if len(self.replycont) > lencoment:
            return '('+ self.replyautor.username + ') ' + self.replycont[:lencoment] + '...'
        else:
            return '('+ self.replyautor.username + ') ' + self.replycont    