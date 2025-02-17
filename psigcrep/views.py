from django.shortcuts import render, redirect, get_object_or_404
from psigcmod.models import Oace, ProgDesarrollo, EntidActor, InfoEjes, Municipio
from itertools import groupby
from django.db.models import Count, Sum
from django.contrib import messages
import json as simplejson
import random 

# Create your views here.


def vista_reportes(request):
    return render(request, "psigcrep/noheaderpage.html")

def count_entidactors(oace, provincia):

    # Assuming you have a 'Municipio' model with a 'province' field
    municipios = Municipio.objects.filter(prov=provincia)
    
    # Get the 'EntidActor' instances for the given 'Oace' and 'Municipio' objects
    entidactors = EntidActor.objects.filter(oace=oace, munic__in=municipios)
    
    # Return the count of 'EntidActor' instances
    return entidactors.count()

def vista_generalidad(request):
    try:
        orgadata = Oace.objects.order_by('siglas').all()
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los OACEs.")
    try:
        progdata = ProgDesarrollo.objects.all()
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar programas de desarrollo.")
    try:
        entidact = EntidActor.objects.order_by('munic__prov__nombreprov', 'munic__nombremun', 'nombrecorto')
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar las Entidades-Actores.")
    try:
        inforegent = InfoEjes.objects.order_by('munic__prov__nombreprov', 'entidactor__nombrecorto', 'munic__nombremun').values('munic__idmun', 'entidactor__idactor', 'munic__prov__nombreprov', 'munic__nombremun','entidactor__nombrecorto').annotate(num_municip=Count('entidactor__munic'))
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos de las Entidades-Actores.")

    return render(request, "psigcrep/tablegeneralrep.html", {"organismos":orgadata, "programas":progdata, 'entidact':entidact, 'inforegent':inforegent})

def vista_reg_entidactores(request):
    if 'url_evalentidactreg' in request.path:
        try:
            inforegent = InfoEjes.objects.order_by('munic__prov__nombreprov', 'entidactor__nombrecorto', 'munic__nombremun').values('entidactor__idactor','munic__idmun','munic__prov__nombreprov', 'munic__nombremun','entidactor__nombrecorto').annotate(num_municip=Count('entidactor__munic')).filter(num_municip__gt=1)
        except:
            messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos de las Entidades-Actores.")
    else:
        try:
            inforegent = InfoEjes.objects.order_by('munic__prov__nombreprov', 'entidactor__nombrecorto', 'munic__nombremun').values('entidactor__idactor','munic__idmun','munic__prov__nombreprov', 'munic__nombremun','entidactor__nombrecorto').annotate(num_municip=Count('entidactor__munic'))
        except:
            messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos de las Entidades-Actores.")
    return render(request, "psigcrep/tableentidactrep.html", {"entidata":inforegent})

def get_proporcion(cant, total):
    if total == 0:
        self = 0
    else:    
        self = round(cant/total*100, 1)
    return self

def vista_indicadores(request, id_entidact, id_mun):
    
    try:
        regdatos = InfoEjes.objects.filter(entidactor=id_entidact, munic=id_mun).order_by('-fechaRegist')
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos. No hay resgistro de esa Entidad-Actor en ese municipio.")
        return redirect('url_indentidactreg')
    try:
        entidact = regdatos[0].entidactor
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos. No existe tal Entidad-Actor en ese municipio.")
        return redirect('url_indentidactreg')

    cantreg = len(regdatos)
    datos = regdatos[0]
    
    total=False
    
    ipgedrec = []
    ipformrec = []
    iporganrec = []
    ipentactrec =[]
    iprelrec =[]

    restoPers = datos.totalPers - datos.cantMujeres

    if datos.totalPers == 0 or datos.cantOC == 0 or datos.cantUniv == 0:
        total = True

    ipFemrec = get_proporcion(datos.cantMujeres, datos.totalPers)
    ip18_35rec = get_proporcion(datos.cant18_35, datos.totalPers)
    ip36_55rec = get_proporcion(datos.cant36_55, datos.totalPers)
    ip56_70rec = get_proporcion(datos.cant56_70, datos.totalPers)
    ip_70rec = get_proporcion(datos.cant_70, datos.totalPers)
    
    ipgedrec = [{'ipFemrec':ipFemrec,'ip18_35rec':ip18_35rec, 'ip36_55rec':ip36_55rec, 'ip56_70rec':ip56_70rec, 'ip36_55rec':ip36_55rec, 'ip_70rec':ip_70rec}]

    ipUnivrec = get_proporcion(datos.cantUniv, datos.totalPers)
    ipTNSrec = get_proporcion(datos.cantTNS, datos.totalPers)
    ipTMrec = get_proporcion(datos.cantTM, datos.totalPers)
    ipObrec = get_proporcion(datos.cantOb, datos.totalPers)
    ipDrCrec= get_proporcion(datos.cantDrC, datos.cantUniv)
    ipMScrec = get_proporcion(datos.cantMSc, datos.cantUniv)
    ipEsPostrec = get_proporcion(datos.cantEsPost, datos.cantUniv)
    ipOC = get_proporcion(datos.cantOC, datos.cantOb)
    
    ipformrec =[{'ipUnivrec':ipUnivrec,'ipTNSrec':ipTNSrec,'ipTMrec':ipTMrec,'ipObrec':ipObrec,
                   'ipDrCrec':ipDrCrec,'ipMScrec':ipMScrec,'ipEsPostrec':ipEsPostrec,
                   'ipOC':ipOC,
                }]
    
    ipICTA = get_proporcion(datos.cantIA_CTA, datos.cantIP_CTA)
    ipPCTI = get_proporcion(datos.cantPECTIC, datos.totalPers)

    iporganrec =[{'ipPCTI':ipPCTI, 'ipICTA':ipICTA, }]

    totalEntProy = datos.cantPAP + datos.cantPNAP + datos.cantPCI + datos.cantPDL + datos.cantPSP
    totalFinan = datos.finanPAP + datos.finanPNAP + datos.finanPCI + datos.finanPDL + datos.finanPSP 
    
    totalRITP = datos.cantRCLA + datos.cantILA + datos.cantTec + datos.cantProc + datos.cantProd
    totalAccExt = datos.cantRDExt + datos.cantRRS + datos.cantAccExt

    if totalEntProy == 0 or totalFinan  == 0 or totalRITP == 0:
        total = True
    

    ipPAP = get_proporcion(datos.cantPAP, totalEntProy)
    ipPNAP = get_proporcion(datos.cantPNAP, totalEntProy)
    ipPCI = get_proporcion(datos.cantPCI, totalEntProy)
    ipPDL = get_proporcion(datos.cantPDL, totalEntProy)
    ipPSP = get_proporcion(datos.cantPSP, totalEntProy)
    ipfinanPAP = get_proporcion(datos.finanPAP, totalFinan)
    ipfinanPNAP = get_proporcion(datos.finanPNAP, totalFinan)
    ipfinanPCI = get_proporcion(datos.finanPCI, totalFinan)
    ipfinanPDL = get_proporcion(datos.finanPDL, totalFinan)
    ipfinanPSP = get_proporcion(datos.finanPSP, totalFinan)

    ipproyrec = [{'totalEntProy':totalEntProy, 'totalFinan':totalFinan,
                    'ipPAP':ipPAP,'ipPNAP':ipPNAP,'ipPCI':ipPCI,'ipPCI':ipPCI,'ipPDL':ipPDL,'ipPSP':ipPSP,
                    'ipPAP':ipPAP,'ipPNAP':ipPNAP,'ipPCI':ipPCI,'ipPDL':ipPDL,'ipPSP':ipPSP,
                    'ipfinanPAP':ipfinanPAP,'ipfinanPNAP':ipfinanPNAP,'ipfinanPCI':ipfinanPCI,'ipfinanPDL':ipfinanPDL,'ipfinanPSP':ipfinanPSP,
                }]

    ipRCLA = get_proporcion(datos.cantRCLA, totalRITP)
    ipILA = get_proporcion(datos.cantILA, totalRITP)
    ipTec = get_proporcion(datos.cantTec, totalRITP)
    ipProc = get_proporcion(datos.cantProc, totalRITP)
    ipProd = get_proporcion(datos.cantProd, totalRITP)
    ipRDExt = get_proporcion(datos.cantRDExt, totalAccExt)
    ipRRS = get_proporcion(datos.cantRRS, totalAccExt)
    ipAccExt = get_proporcion(datos.cantAccExt, totalAccExt)
    ipRING = get_proporcion(datos.cantRING, totalAccExt)
    ipPDiv = get_proporcion(datos.cantPDiv, datos.totalPers)

    iprelrec = [{'totalRITP':totalRITP,'ipRCLA':ipRCLA,'ipILA':ipILA,'ipTec':ipTec,'ipProc':ipProc,'ipProd':ipProd,
                  'totalAccExt':totalAccExt,'ipRDExt':ipRDExt,'ipRRS':ipRRS, 'ipAccExt':ipAccExt, 'ipRING':ipRING, 'ipPDiv':ipPDiv
                }]

    if total:
        messages.add_message(request=request, level=messages.ERROR, message="Algunos de los valores que representan o se calculan como totales son nulos. Es posible que no se obtengan los resultados esperados.")
        messages.add_message(request=request, level=messages.SUCCESS, message="Verifique los datos primarios de los registros del entidad-actor para este municipio .")

    return render(request, "psigcrep/tablaprop.html", {'cantreg':cantreg,'idmuni':id_mun,'identidact':id_entidact,'datrec':datos,
                                                       'ipgedrec':ipgedrec, 'ipforsupcap':ipformrec, 'iporganrec':iporganrec, 'ipproyrec':ipproyrec, 'iprelrec':iprelrec})

def dcrec(dat1, dat2):
    dc= round((dat2-dat1)/dat1*100,1)
    return(dc)

def asignarind(dc):
    if dc < -50:
        ind = -1
    if dc >= -50 and dc < 0:
        ind = -0.5
    if dc == 0:
        ind = 0    
    if dc > 0 and dc < 50:
        ind = 0.5
    if dc >= 50:
        ind = 1
    if dc> 100:
        ind = 2
    return (ind)

def vista_evaluaciones(request, id_entidact, id_mun):
        
    try:
        regdatos = InfoEjes.objects.filter(entidactor=id_entidact, munic=id_mun).order_by('-fechaRegist')
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos. No existe tal Entidad-Actor en ese municipio.")
        return redirect('url_evalentidactreg')
    print(regdatos)
    try:
        entidact = regdatos[0].entidactor
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos. No existe tal Entidad-Actor en ese municipio.")
        return redirect('url_evalentidactreg')
    try:
        entidact = regdatos[0].munic
    except:
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos. No existe tal Entidad-Actor en ese municipio.")
        return redirect('url_evalentidactreg')
    
    cantreg = len(regdatos)
    
    if cantreg>1:
        datoeval = regdatos[0]
        datobas = regdatos[0]
    else:
        messages.add_message(request=request, level=messages.ERROR, message="La Entidad-Actor seleccionada no tiene más de 1 registro en ese municipio.")
        return redirect('url_evalentidactreg')
    
    fechabas=False
    for dat in regdatos:
        if dat.fechabase:
            datobas = dat
            fechabas = True
    
    if  not fechabas:
        messages.add_message(request=request, level=messages.SUCCESS, message="No se ha especificado fecha base para la evaluación. PSIGC asumirá la primera fecha de registro de datos")
        datobas = dat
    
    indparcform = []
    indparcorganiz = []
    indparcgest = []
    indparcrelac = []
    indejes = []
##
    ipUniv = round(get_proporcion(datoeval.cantUniv, datoeval.totalPers) - get_proporcion(datobas.cantUniv, datobas.totalPers), 2)
    if datobas.cantUniv != 0:
        dcUniv = dcrec(datobas.cantUniv, datoeval.cantUniv)
    else:
        dcUniv = get_proporcion(datoeval.cantUniv, datoeval.totalPers)
#
    ipTNS = round(get_proporcion(datoeval.cantTNS, datoeval.totalPers) - get_proporcion(datobas.cantTNS, datobas.totalPers), 2)
    if datobas.cantTNS != 0:
        dcTNS = dcrec( datobas.cantTNS, datoeval.cantTNS)
    else:
        dcTNS = get_proporcion(datoeval.cantTNS, datoeval.totalPers)
#
    ipTM = round(get_proporcion(datoeval.cantTM, datoeval.totalPers) -  get_proporcion(datobas.cantTM, datobas.totalPers), 2)
    if datobas.cantTM != 0:
        dcTM = dcrec(datobas.cantTM, datoeval.cantTM)
    else:
        dcTM = get_proporcion(datoeval.cantTM, datoeval.totalPers)
#
    ipOb = round(get_proporcion(datoeval.cantOb, datoeval.totalPers) - get_proporcion(datobas.cantOb, datobas.totalPers), 2)
    if datobas.cantOb != 0:
        dcOb = dcrec(datobas.cantOb, datoeval.cantOb)
    else:
        dcOb = get_proporcion(datoeval.cantOb, datoeval.totalPers)
#
    ippform = round((ipUniv + ipTNS + ipTM + ipOb)/4, 2)
    dcform = round((dcUniv + dcTNS + dcTM + dcOb)/4, 2)
##
    ipDrC = round(get_proporcion(datoeval.cantDrC, datoeval.cantUniv) - get_proporcion(datobas.cantDrC, datobas.cantUniv), 2)
    if datobas.cantDrC != 0:
        dcDrC = dcrec(datobas.cantDrC, datoeval.cantDrC)
    else:
        dcDrC = get_proporcion(datoeval.cantDrC, datoeval.cantUniv)
#
    ipMSc =  round(get_proporcion(datoeval.cantMSc, datoeval.cantUniv) - get_proporcion(datobas.cantMSc, datobas.cantUniv), 2)
    if datobas.cantMSc != 0:
        dcMSc = dcrec(datobas.cantMSc, datoeval.cantMSc)
    else:
        dcMSc = get_proporcion(datoeval.cantMSc, datoeval.cantUniv)
#
    ipEsPost =  round(get_proporcion(datoeval.cantEsPost, datoeval.cantUniv) - get_proporcion(datobas.cantEsPost, datobas.cantUniv), 2)
    if datobas.cantEsPost != 0:
        dcEsPost = dcrec(datobas.cantEsPost, datoeval.cantEsPost)
    else:
        dcEsPost = get_proporcion(datoeval.cantEsPost, datoeval.cantUniv)
#    
    ippsup = round(( ipDrC + ipMSc + ipEsPost)/3, 2)
    dcsup = round(( dcDrC + dcMSc + dcEsPost)/3, 2)
##
    ipCuadCap = round(get_proporcion(datoeval.cantCuadCap, datoeval.cantUniv+datoeval.cantTNS) - get_proporcion(datobas.cantCuadCap, datobas.cantUniv+datobas.cantTNS), 2)
    if datobas.cantCuadCap != 0:
        dcCuadCap = dcrec(datobas.cantCuadCap, datoeval.cantCuadCap)
    else:
        dcCuadCap = get_proporcion(datoeval.cantCuadCap, datoeval.cantUniv+datoeval.cantTNS)
#
    ipResCuad = round(get_proporcion(datoeval.cantResCuad, datoeval.cantUniv+datoeval.cantTNS) - get_proporcion(datobas.cantResCuad, datobas.cantUniv+datobas.cantTNS), 2)
    if datobas.cantResCuad != 0:
        dcResCuad = dcrec(datobas.cantResCuad, datoeval.cantResCuad)
    else:
        dcResCuad = get_proporcion(datoeval.cantResCuad, datoeval.cantUniv+datoeval.cantTNS)
#
    ipEspCap = round(get_proporcion(datoeval.cantEspCap, datoeval.cantUniv+datoeval.cantTNS) - get_proporcion(datobas.cantEspCap, datobas.cantUniv+datobas.cantTNS), 2)
    if datobas.cantEspCap != 0:
        dcEspCap = dcrec(datobas.cantEspCap, datoeval.cantEspCap)
    else:
        dcEspCap = get_proporcion(datoeval.cantEspCap, datoeval.cantUniv+datoeval.cantTNS)
#
    ipPrdCap = round(get_proporcion(datoeval.cantPrdCap, datoeval.totalPers) - get_proporcion(datobas.cantPrdCap, datobas.totalPers), 2)
    if datobas.cantPrdCap != 0:
        dcPrdCap = dcrec(datobas.cantPrdCap, datoeval.cantPrdCap)
    else:
        dcPrdCap =  get_proporcion(datoeval.cantPrdCap, datoeval.totalPers)
#
    ipOC = round(get_proporcion(datoeval.cantOC, datoeval.cantOb) - get_proporcion(datobas.cantOC, datobas.cantOb), 2)
    if datobas.cantOC != 0:
        dcOC = dcrec(datobas.cantOC, datoeval.cantOC)
    else:
        dcOC =  get_proporcion(datoeval.cantOC, datoeval.cantOb)
#
    ippcap = round((ipCuadCap + ipResCuad + ipEspCap + ipPrdCap + ipOC)/5, 2)
    dccap = round((dcCuadCap + dcResCuad + dcEspCap + dcPrdCap + dcOC)/5, 2)

    indparcform = [{'ipUniv':ipUniv, 'ipTNS':ipTNS, 'ipTM':ipTM, 'ipOb':ipOb, 'ippform':ippform,
                    'dcUniv':dcUniv, 'dcTNS':dcTNS, 'dcTM':dcTM, 'dcOb':dcOb, 'dcform':dcform,
                    'ipDrC':ipDrC, 'ipMSc':ipMSc, 'ipEsPost':ipEsPost, 'ippsup':ippsup,
                    'dcDrC':dcDrC, 'dcMSc':dcMSc, 'dcEsPost':dcEsPost, 'dcsup':dcsup,
                    'ipCuadCap':ipCuadCap, 'ipResCuad':ipResCuad, 'ipEspCap':ipEspCap, 'ipPrdCap':ipPrdCap, 'ipOC':ipOC, 'ippcap':ippcap,
                    'dcCuadCap':dcCuadCap, 'dcResCuad':dcResCuad, 'dcEspCap':dcEspCap, 'dcPrdCap':dcPrdCap, 'dcOC':dcOC, 'dccap':dccap,
                    }]
    
    ippintelec = round((ipUniv + ipTNS + ipTM + ipMSc + ipEsPost + ipDrC + ipCuadCap + ipResCuad + ipEspCap + ipPrdCap + ipOC)/11, 2)

####
    ipCTA = round(get_proporcion(datoeval.cantCTA, datoeval.cantCTA+datoeval.cantECTI) - get_proporcion(datobas.cantCTA, datobas.cantCTA+datobas.cantECTI), 2)
    if datobas.cantCTA != 0:
        dcCTA = dcrec(datobas.cantCTA, datoeval.cantCTA)
    else:
        dcCTA = get_proporcion(datoeval.cantCTA, datoeval.cantCTA+datoeval.cantECTI)
#
    ipECTI = round(get_proporcion(datoeval.cantECTI, datoeval.cantCTA+datoeval.cantECTI) - get_proporcion(datobas.cantECTI, datobas.cantCTA+datobas.cantECTI), 2)
    if datobas.cantECTI != 0:
        dcECTI = dcrec(datobas.cantECTI, datoeval.cantECTI)
    else:
        dcECTI = get_proporcion(datoeval.cantECTI, datoeval.cantCTA+datoeval.cantECTI)
#
    if datobas.cantIP_CTA != 0:
        ipIPCTA = get_proporcion(datoeval.cantIP_CTA, datobas.cantIP_CTA)
        dcIPCTA = dcrec(datobas.cantIP_CTA, datoeval.cantIP_CTA)
    else:
        ipIPCTA = get_proporcion(datoeval.cantIP_CTA, datoeval.cantIP_CTA)
        dcIPCTA = ipIPCTA
#
    ipIACTA = round(get_proporcion(datoeval.cantIA_CTA, datoeval.cantIP_CTA) - get_proporcion(datobas.cantIA_CTA, datobas.cantIP_CTA), 2)
    if datobas.cantIA_CTA != 0:
        dcIACTA = dcrec(datobas.cantIA_CTA, datoeval.cantIA_CTA)
    else:
        dcIACTA = get_proporcion(datoeval.cantIA_CTA, datoeval.cantIP_CTA)
#
    ipPECTI =  round(get_proporcion(datoeval.cantPECTIC, datoeval.totalPers) - get_proporcion(datobas.cantPECTIC, datobas.totalPers), 2)
    if datobas.cantPECTIC != 0:
        dcPECTI = dcrec(datobas.cantPECTIC, datoeval.cantPECTIC)
    else:
        dcPECTI = get_proporcion(datoeval.cantPECTIC, datoeval.totalPers)
##
    ippINNOV = round((ipIPCTA + ipIACTA)/2, 2)
    dcINNOV = round((dcIPCTA + dcIACTA)/2, 2)

    ippECTA = round((ipCTA + ipECTI + ipPECTI)/3, 2)
    dcECTA = round((dcCTA + dcECTI)/2, 2)

    indparcorganiz = [{'ipcta':ipCTA,'ipipcta':ipIPCTA,'ipiacta':ipIACTA, 'ipecti':ipECTI, 'ippecti':ipPECTI, 
                       'ippinnov':ippINNOV, 'ippecta':ippECTA,
                        'dccta':dcCTA, 'dcipcta':dcIPCTA, 'dciacta':dcIACTA, 'dcecti':dcECTI, 'dcpecti':dcPECTI,
                        'dcinnov':dcINNOV, 'dcecta':dcECTA
                        }]

    ipporganiz = round((ipCTA + ipIPCTA + ipIACTA + ipECTI + ipPECTI)/5, 2)

####
    totalProyB = datobas.cantPAP + datobas.cantPNAP + datobas.cantPCI + datobas.cantPDL + datobas.cantPSP
    totalFinanB = datobas.finanPAP + datobas.finanPNAP + datobas.finanPCI + datobas.finanPDL + datobas.finanPSP 

    totalProyE = datoeval.cantPAP + datoeval.cantPNAP + datoeval.cantPCI + datoeval.cantPDL + datoeval.cantPSP
    totalFinanE = datoeval.finanPAP + datoeval.finanPNAP + datoeval.finanPCI + datoeval.finanPDL + datoeval.finanPSP   
#
    ipPAP = round(get_proporcion(datoeval.cantPAP, totalProyE) - get_proporcion(datobas.cantPAP, totalProyB), 2)
    if datobas.cantPAP != 0:
        dcPAP = dcrec(datobas.cantPAP, datoeval.cantPAP)
    else:
        dcPAP = get_proporcion(datoeval.cantPAP,  totalProyE)
#
    ipPNAP = round(get_proporcion(datoeval.cantPNAP, totalProyE) - get_proporcion(datobas.cantPNAP, totalProyB), 2)
    if datobas.cantPNAP != 0:
        dcPNAP = dcrec(datobas.cantPNAP, datoeval.cantPNAP)
    else:
        dcPNAP = get_proporcion(datoeval.cantPNAP,  totalProyE)
#
    ipPCI = round(get_proporcion(datoeval.cantPCI, totalProyE) - get_proporcion(datobas.cantPCI, totalProyB), 2)
    if datobas.cantPCI != 0:
        dcPCI = dcrec(datobas.cantPCI,  datoeval.cantPCI)
    else:
        dcPCI = get_proporcion(datoeval.cantPCI,  totalProyE)
#
    ipPDL = round(get_proporcion(datoeval.cantPDL, totalProyE) - get_proporcion(datobas.cantPDL, totalProyB), 2)
    if datobas.cantPDL != 0:
        dcPDL = dcrec(datobas.cantPDL, datoeval.cantPDL)
    else:
        dcPDL = get_proporcion(datoeval.cantPDL,  totalProyE)
#
    ipPSP = round(get_proporcion(datoeval.cantPSP, totalProyE) - get_proporcion(datobas.cantPSP, totalProyB), 2)
    if datobas.cantPSP != 0:
        dcPSP = dcrec(datobas.cantPSP, datoeval.cantPSP)
    else:
        dcPSP = get_proporcion(datoeval.cantPSP,  totalProyE)
##
    ippProy = round((ipPAP + ipPNAP + ipPCI + ipPDL + ipPSP)/5, 2)
    dcProy = round((dcPAP + dcPNAP + dcPCI + dcPDL + dcPSP)/5, 2)
#
    ipfPAP = round(get_proporcion(datoeval.finanPAP, totalFinanE) - get_proporcion(datobas.finanPAP, totalFinanB), 2)
    if datobas.finanPAP != 0:
        dcfPAP = dcrec(datobas.finanPAP, datoeval.finanPAP)
    else:
        dcfPAP = get_proporcion(datoeval.finanPAP,  totalFinanE)
#
    ipfPNAP = round(get_proporcion(datoeval.finanPNAP, totalFinanE) - get_proporcion(datobas.finanPNAP, totalFinanB), 2)
    if datobas.finanPNAP != 0:
        dcfPNAP = dcrec(datobas.finanPNAP, datoeval.finanPNAP)
    else:
        dcfPNAP = get_proporcion(datoeval.finanPNAP,  totalFinanE)
#
    ipfPCI = round(get_proporcion(datoeval.finanPCI, totalFinanE) - get_proporcion(datobas.finanPCI, totalFinanB), 2)
    if datobas.finanPCI != 0:
        dcfPCI = dcrec(datobas.finanPCI,  datoeval.finanPCI)
    else:
        dcfPCI = get_proporcion(datoeval.finanPCI,  totalFinanE)
#
    ipfPDL = round(get_proporcion(datoeval.finanPDL, totalFinanE) - get_proporcion(datobas.finanPDL, totalFinanB), 2)
    if datobas.finanPDL != 0:
        dcfPDL = dcrec(datobas.finanPDL, datoeval.finanPDL)
    else:
        dcfPDL = get_proporcion(datoeval.finanPDL,  totalFinanE)
#    
    ipfPSP = round(get_proporcion(datoeval.finanPSP, totalFinanE) - get_proporcion(datobas.finanPSP, totalFinanB), 2)
    if datobas.finanPSP != 0:
        dcfPSP = dcrec(datobas.finanPSP, datoeval.finanPSP)
    else:
        dcfPSP = get_proporcion(datoeval.finanPSP,  totalFinanE)
    
    ippFinan = round((ipfPAP + ipfPNAP + ipfPCI + ipfPDL + ipfPSP)/5, 2)
    dcFinan = round((dcfPAP + dcfPNAP + dcfPCI + dcfPDL + dcfPSP)/5, 2)
#    
    ipfPSP = round(get_proporcion(datoeval.finanPSP, totalFinanE) - get_proporcion(datobas.finanPSP, totalFinanB), 2)
    if datobas.finanPSP != 0:
        dcfPSP = dcrec(datobas.finanPSP, datoeval.finanPSP)
    else:
        dcfPSP = get_proporcion(datoeval.finanPSP,  totalFinanE)

    indparcgest = [{'ippap':ipPAP, 'ippnap':ipPNAP, 'ippci':ipPCI, 'ippdl':ipPDL, 'ippsp':ipPSP, 'ippproy':ippProy,
                    'dcpap':dcPAP, 'dcpnap':dcPNAP, 'dcpci':dcPCI, 'dcpdl':dcPDL, 'dcpsp':dcPSP, 'dcproy':dcProy,
                    'ipfpap':ipfPAP, 'ipfpnap':ipfPNAP, 'ipfpci':ipfPCI, 'ipfpdl':ipfPDL, 'ipfpsp':ipfPSP, 'ippfinan':ippFinan,
                    'dcfpap':dcfPAP, 'dcfpnap':dcfPNAP, 'dcfpci':dcfPCI, 'dcfpdl':dcfPDL, 'dcfpsp':dcfPSP, 'dcfinan':dcFinan
                    }]
    
    ippgest = round((ipPAP + ipPNAP + ipPCI + ipPDL + ipPSP + ipfPAP + ipfPNAP + ipfPCI + ipfPDL + ipfPSP)/10, 2)

#####
    totalRITPB =  datobas.cantRCLA + datobas.cantILA + datobas.cantTec + datobas.cantProc + datobas.cantProd
    totalRITPE = datoeval.cantRCLA + datoeval.cantILA + datoeval.cantTec + datoeval.cantProc + datoeval.cantProd

    totalExtB = datobas.cantRDExt + datobas.cantRRS + datobas.cantAccExt + datobas.cantRING + datobas.cantPDiv
    totalExtE = datoeval.cantRDExt + datoeval.cantRRS + datoeval.cantAccExt + datoeval.cantRING + datoeval.cantPDiv
    
#
    ipRCLA = round(get_proporcion(datoeval.cantRCLA, totalRITPE) - get_proporcion(datobas.cantRCLA, totalRITPB), 2)
    if datobas.cantRCLA != 0:
        dcRCLA = dcrec(datobas.cantRCLA, datoeval.cantRCLA)
    else:
        dcRCLA = get_proporcion(datoeval.cantRCLA,  totalRITPE)
#
    ipILA = round(get_proporcion(datoeval.cantILA, totalRITPE) - get_proporcion(datobas.cantILA, totalRITPB), 2)
    if datobas.cantILA != 0:
        dcILA = dcrec(datobas.cantILA, datoeval.cantILA)
    else:
        dcILA = get_proporcion(datoeval.cantILA, totalRITPE)
#
    ipTec = round(get_proporcion(datoeval.cantTec, totalRITPE) - get_proporcion(datobas.cantTec, totalRITPB), 2)
    if datobas.cantTec != 0:
        dcTec = dcrec(datobas.cantTec, datoeval.cantTec)
    else:
        dcTec = get_proporcion(datoeval.cantTec,  totalRITPE)
#
    ipProc = round(get_proporcion(datoeval.cantProc, totalRITPE) - get_proporcion(datobas.cantProc, totalRITPB), 2)
    if datobas.cantProc != 0:
        dcProc = dcrec(datobas.cantProc, datoeval.cantProc)
    else:
        dcProc = get_proporcion(datoeval.cantProc,  totalRITPE)
#
    ipProd = round(get_proporcion(datoeval.cantProd, totalRITPE) - get_proporcion(datobas.cantProd, totalRITPB), 2)
    if datobas.cantProd != 0:
        dcProd = dcrec(datobas.cantProd, datoeval.cantProd)
    else:
        dcProd = get_proporcion(datoeval.cantTec,  totalRITPE)
    
    ippRITP = round((ipRCLA + ipILA + ipTec + ipProc + ipProd)/5, 2)
    dcRITP = round((dcRCLA + dcILA + dcTec + dcProc + dcProd)/5, 2)

##
    ipRDExt = round(get_proporcion(datoeval.cantRDExt, totalExtE) - get_proporcion(datobas.cantRDExt, totalExtB), 2)
    if datobas.cantRDExt != 0:
        dcRDExt = dcrec(datobas.cantProd, datoeval.cantProd)
    else:
        dcRDExt = get_proporcion(datoeval.cantRDExt,  totalExtE)
#
    ipRRS = round(get_proporcion(datoeval.cantRRS, totalExtE) - get_proporcion(datobas.cantRRS, totalExtB), 2)
    if datobas.cantRRS != 0:
        dcRRS = dcrec(datobas.cantRRS, datoeval.cantRRS)
    else:
        dcRRS = get_proporcion(datoeval.cantRRS,  totalExtE)    
#
    ipAccExt = round(get_proporcion(datoeval.cantAccExt, totalExtE) - get_proporcion(datobas.cantAccExt, totalExtB), 2)
    if datobas.cantAccExt != 0:
        dcAccExt = dcrec(datobas.cantAccExt, datoeval.cantAccExt)
    else:
        dcAccExt = get_proporcion(datoeval.cantAccExt,  totalExtE)
#
    ipRing = round(get_proporcion(datoeval.cantRING, totalExtE) - get_proporcion(datobas.cantRING, totalExtB), 2)
    if datobas.cantRING != 0:
        dcRing = dcrec(datobas.cantRING, datoeval.cantRING)
    else:
        dcRing = get_proporcion(datoeval.cantRING,  totalExtE)
#
    ipPDiv = round(get_proporcion(datoeval.cantPDiv, datoeval.totalPers) - get_proporcion(datobas.cantPDiv, datoeval.totalPers), 2)
    if datobas.cantPDiv != 0:
        dcPDiv = dcrec(datobas.cantPDiv, datoeval.cantPDiv)
    else:
        dcPDiv = get_proporcion(datoeval.cantPDiv,  datoeval.totalPers)

    ippExt = round((ipRDExt + ipRRS + ipAccExt + ipRing + ipPDiv)/5, 2)
    dcExt = round(( dcRDExt + dcRRS + dcAccExt + dcRing + dcPDiv)/5, 2)
    
    indparcrelac = [{'iprcla':ipRCLA,'ipila':ipILA,'iptec':ipTec,'ipproc':ipProc,'ipprod':ipProd,'ippritp':ippRITP, 
                    'dcrcla':dcRCLA,'dcila':dcILA,'dctec':dcTec,'dcproc':dcProc,'dcprod':dcProd,'dcritp':dcRITP,
                    'iprdext':ipRDExt, 'iprrs':ipRRS, 'ipaccext':ipAccExt, 'ipring':ipRing, 'ippdiv':ipPDiv, 'ippext':ippExt,
                    'dcrdext':dcRDExt, 'dcrrs':dcRRS, 'dcaccext':dcAccExt, 'dcring':dcRing, 'dcpdiv':dcPDiv, 'dcext':dcExt
                   }]

    ipprelac = round( (ipRCLA + ipILA + ipTec + ipProc + ipProd + ipRDExt + ipRRS + ipAccExt + ipRing + ipPDiv)/10, 2)
    dcrelac = round((dcRCLA + dcILA + dcTec + dcProc + dcProd + dcRDExt + dcRRS + dcAccExt + dcRing + dcPDiv)/10, 2)

    indejes = [{'ippintelec':ippintelec, 'ipporganiz':ipporganiz, 'ippgest':ippgest, 'ipprelac':ipprelac }]

    return render(request, "psigcrep/tablaeval.html", {'identidact':id_entidact, 'idmun':id_mun, 'datoeval':datoeval, 'datobas':datobas, 
                                                       'indparcform':indparcform, 'indparcorganiz':indparcorganiz, 'indparcgest':indparcgest, 'indparcrelac':indparcrelac, 
                                                       'indejes':indejes})

def vista_regentimunic(request, id_entid, id_munic):
    try:
        regdatos = InfoEjes.objects.filter(entidactor=id_entid, munic=id_munic)
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos. No existe tal Entidad-Actor en ese municipio.")
        return redirect('url_general')  
    try:
        entidact = regdatos[0].entidactor.nombrecorto
    except: 
        messages.add_message(request=request, level=messages.ERROR, message="Error al intentar cargar los datos. No existe tal Entidad-Actor en ese municipio.")
        return redirect('url_general')
    
    munic = regdatos[0].munic.nombremun
    prov = regdatos[0].munic.prov.nombreprov
    regpers = []
    regform = []
    regorganiz = []
    reggest = []
    regrelac = []
    cantreg = len(regdatos)    
    for reg in regdatos:
        regpers.append({'fecha':reg.fechaRegist, 'fechabase':reg.fechabase,'totalPers':reg.totalPers, 'cantMujeres':reg.cantMujeres, 'cant18_35':reg.cant18_35, 'cant36_55':reg.cant36_55, 'cant56_70':reg.cant56_70, 'cant_70':reg.cant_70})
        regform.append({ 'fecha':reg.fechaRegist,'fechabase':reg.fechabase,'cantUniv':reg.cantUniv, 'cantTNS':reg.cantTNS, 'cantTM':reg.cantTM, 'cantOb':reg.cantOb, 'cantDrC':reg.cantDrC, 'cantMSc':reg.cantMSc, 'cantEsPost':reg.cantEsPost, 'cantCuadCap':reg.cantCuadCap, 'cantResCuad':reg.cantResCuad, 'cantEspCap':reg.cantEspCap, 'cantPrdCap':reg.cantPrdCap, 'cantOC':reg.cantOC})
        regorganiz.append({'fecha':reg.fechaRegist,'fechabase':reg.fechabase,'cantPECTIC':reg.cantPECTIC, 'cantCTA':reg.cantCTA, 'cantECTI':reg.cantECTI, 'cantIP_CTA':reg.cantIP_CTA, 'cantIA_CTA':reg.cantIA_CTA,})
        reggest.append({'fecha':reg.fechaRegist,'fechabase':reg.fechabase,'cantPAP':reg.cantPAP, 'cantPNAP':reg.cantPNAP, 'cantPCI':reg.cantPCI, 'cantPDL':reg.cantPDL, 'cantPSP':reg.cantPSP, 'finanPAP':reg.finanPAP, 'finanPNAP':reg.finanPNAP, 'finanPCI':reg.finanPCI, 'finanPDL':reg.finanPDL, 'finanPSP':reg.finanPSP})
        regrelac.append({'fecha':reg.fechaRegist,'fechabase':reg.fechabase,'cantRCLA':reg.cantRCLA, 'cantILA':reg.cantILA, 'cantTec':reg.cantTec, 'cantProc':reg.cantProc, 'cantProd':reg.cantProd, 'cantRDExt':reg.cantRDExt, 'cantRRS':reg.cantRRS,'cantAccExt':reg.cantAccExt, 'cantRING':reg.cantRING, 'cant':reg.cantRCLA, 'cantPDiv':reg.cantPDiv})
       
    return render(request, "psigcrep/regisentmunic.html", {'cantreg':cantreg, 'identidact':id_entid,'entidact':entidact, 'idmuni':id_munic,'munic':munic, 'prov':prov, 'regpers':regpers, 'regform':regform, 'regorganiz':regorganiz, 'reggest':reggest, 'regrelac':regrelac })

def vista_conocasist(request):
    return render(request, "psigcrep/noheaderpage.html")
