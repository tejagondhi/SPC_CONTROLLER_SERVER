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
            TCWL = list(map(float,data.values_list('TCWL',flat=True)))
            TCWR = list(map(float,data.values_list('TCWR',flat=True)))
            BCWL = list(map(float,data.values_list('BCWL',flat=True)))
            BCWR = list(map(float,data.values_list('BCWR',flat=True)))
            TotalThickness = list(map(float,data.values_list('TotalThickness',flat=True)))
            TopTotalWidth = list(map(float,data.values_list('TopTotalWidth',flat=True)))
            BottomTotalWidth = list(map(float,data.values_list('BottomTotalWidth',flat=True)))
            FinalTotalWidth = list(map(float,data.values_list('FinalTotalWidth',flat=True)))
            for f in os.listdir(settings.MEDIA_ROOT):
                os.remove(os.path.join(settings.MEDIA_ROOT, f))
            uniqueId = uuid4()
            generateGraphs(TCWL,"Top Champher Left", "TCWL", "Frequency", settings.MEDIA_ROOT + "\\TCWL_"+str(uniqueId)+".png")
            generateGraphs(TCWR,"Top Champher Right", "TCWR", "Frequency", settings.MEDIA_ROOT + "\\TCWR_"+str(uniqueId)+".png")
            generateGraphs(BCWL,"Bottom champher Left", "BCWL", "Frequency", settings.MEDIA_ROOT + "\\BCWL_"+str(uniqueId)+".png")
            generateGraphs(BCWR,"Bottom Champher Right", "BCWR", "Frequency", settings.MEDIA_ROOT + "\\BCWR_"+str(uniqueId)+".png")
            generateGraphs(TotalThickness,"Total Thickness", "TotalThickness", "Frequency", settings.MEDIA_ROOT + "\\TotalThickness_"+str(uniqueId)+".png")
            generateGraphs(TopTotalWidth,"Total Top Width", "TopTotalWidth", "Frequency", settings.MEDIA_ROOT + "\\TopTotalWidth_"+str(uniqueId)+".png")
            generateGraphs(BottomTotalWidth,"Total Bottom Width", "BottomTotalWidth", "Frequency", settings.MEDIA_ROOT + "\\BottomTotalWidth_"+str(uniqueId)+".png")
            generateGraphs(FinalTotalWidth,"Total Width", "FinalTotalWidth", "Frequency", settings.MEDIA_ROOT + "\\FinalTotalWidth_"+str(uniqueId)+".png")
        except Exception as e:
            print(e)
            response = HttpResponse('some data')
            response.status_code = 500  # sample status code
            return response
        responseData = ["TCWL_"+str(uniqueId)+".png","TCWR_"+str(uniqueId)+".png","BCWL_"+str(uniqueId)+".png","BCWR_"+str(uniqueId)+".png","TotalThickness_"+str(uniqueId)+".png","TopTotalWidth_"+str(uniqueId)+".png","BottomTotalWidth_"+str(uniqueId)+".png","FinalTotalWidth_"+str(uniqueId)+".png"]
        return JsonResponse(responseData, safe=False)


