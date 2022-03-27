from importlib.metadata import metadata
import re
from telnetlib import STATUS
from time import sleep
from uuid import uuid4
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from MainController.models import MetaData
from MainController.models import getPlankDataModel
from MainController.models import MeasuresData
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from MainController.plotGenerator import generateGraphs
import datetime
import os
# Create your views here.
#request handler
@csrf_exempt
def render_main(request):
    return render(request, 'index.html')

@csrf_exempt
def search(request):
    if (request.method == "POST"):

        data = MetaData.objects.all()
        if(len(request.POST.get('mode','')) > 0) :
            data = data.filter(Mode = request.POST.get('mode',''))
        
        if(len(request.POST.get('operator','')) > 0) :
            data = data.filter(Operator = request.POST.get('operator',''))

        if(len(request.POST.get('bladeId','')) > 0) :
            data = data.filter(BladeID = request.POST.get('bladeId',''))

        if(len(request.POST.get('bladeType','')) > 0) :
            data = data.filter(BladeType = request.POST.get('bladeType',''))
        
        if(len(request.POST.get('coilId','')) > 0) :
            data = data.filter(CoilID = request.POST.get('coilId',''))

        if(len(request.POST.get('batchNumber','')) > 0) :
            data = data.filter(BatchNumber = request.POST.get('batchNumber',''))

        if(len(request.POST.get('date','')) > 0) :
            data = data.filter(Date = datetime.datetime.strptime(request.POST.get('date',''), '%Y-%m-%d').strftime('%d-%m-%Y'))

        if(len(data) <= 0) :
            response = HttpResponse('some data')
            response.status_code = 500  # sample status code
            return response
        serialized_queryset = serializers.serialize('json', data)
        return JsonResponse(serialized_queryset, safe=False)

@csrf_exempt
def getGraphs(request):
    if (request.method == "POST"):
        try :
            plankId = request.POST.get('id','')
            plankPrefix = "00000"
            plankTableName = "plank_" + plankPrefix[:-len(str(plankId))] + str(plankId)
            plankData = getPlankDataModel(plankTableName)
            plankData._meta.db_table = plankTableName
            data = plankData.objects.all()
            measureObj = MeasuresData.objects.get(ID = 1)
            TCWL = list(map(float,data.values_list('TCWL',flat=True)))
            TCWR = list(map(float,data.values_list('TCWR',flat=True)))
            BCWL = list(map(float,data.values_list('BCWL',flat=True)))
            BCWR = list(map(float,data.values_list('BCWR',flat=True)))
            ThicknessLeft = list(map(float,data.values_list('ThicknessLeft',flat=True)))
            TopWidth = list(map(float,data.values_list('TopWidth',flat=True)))
            BottomWidth = list(map(float,data.values_list('BottomWidth',flat=True)))
            ThicknessRight = list(map(float,data.values_list('ThicknessRight',flat=True)))
            for f in os.listdir(settings.MEDIA_ROOT):
                os.remove(os.path.join(settings.MEDIA_ROOT, f))
            uniqueId = uuid4()
            generateGraphs(TCWL,"Top Chamfer Left", "TCWL", "Frequency", settings.MEDIA_ROOT + "\\TCWL_"+str(uniqueId)+".png",measureObj.TopChamferWidthLeft_LDL,measureObj.TopChamferWidthLeft_UDL)
            generateGraphs(TCWR,"Top Chamfer Right", "TCWR", "Frequency", settings.MEDIA_ROOT + "\\TCWR_"+str(uniqueId)+".png",measureObj.TopChamferWidthRight_LDL,measureObj.TopChamferWidthRight_UDL)
            generateGraphs(BCWL,"Bottom Chamfer Left", "BCWL", "Frequency", settings.MEDIA_ROOT + "\\BCWL_"+str(uniqueId)+".png",measureObj.BottomChamferWidthLeft_LDL,measureObj.BottomChamferWidthLeft_UDL)
            generateGraphs(BCWR,"Bottom Chamfer Right", "BCWR", "Frequency", settings.MEDIA_ROOT + "\\BCWR_"+str(uniqueId)+".png",measureObj.BottomChamferWidthRight_LDL,measureObj.BottomChamferWidthRight_UDL)
            generateGraphs(ThicknessLeft,"Thickness Left", "Thickness Left", "Frequency", settings.MEDIA_ROOT + "\\ThicknessLeft_"+str(uniqueId)+".png",measureObj.ThicknessLeft_LDL,measureObj.ThicknessLeft_UDL)
            generateGraphs(ThicknessRight,"Thickness Right", "Thickness Right", "Frequency", settings.MEDIA_ROOT + "\\ThicknessRight_"+str(uniqueId)+".png",measureObj.ThicknessRight_LDL,measureObj.ThicknessRight_UDL)
            generateGraphs(TopWidth,"Top Width", "Top Width", "Frequency", settings.MEDIA_ROOT + "\\TopWidth_"+str(uniqueId)+".png",measureObj.TopWidth_LDL,measureObj.TopWidth_UDL)
            generateGraphs(BottomWidth,"Bottom Width", "Bottom Width", "Frequency", settings.MEDIA_ROOT + "\\BottomWidth_"+str(uniqueId)+".png",measureObj.BottomWidth_LDL,measureObj.BottomWidth_UDL)
        except Exception as e:
            print(e)
            response = HttpResponse('some data')
            response.status_code = 500  # sample status code
            return response
        responseData = ["TCWL_"+str(uniqueId)+".png","TCWR_"+str(uniqueId)+".png","BCWL_"+str(uniqueId)+".png","BCWR_"+str(uniqueId)+".png","ThicknessLeft_"+str(uniqueId)+".png","ThicknessRight_"+str(uniqueId)+".png","TopWidth_"+str(uniqueId)+".png","BottomWidth_"+str(uniqueId)+".png"]
        return JsonResponse(responseData, safe=False)


