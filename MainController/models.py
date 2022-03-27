import imp
from django.db import models
from django import forms

# Create your models here.
class MetaData(models.Model):   
    ID = models.BigIntegerField()
    Mode = models.CharField(max_length=100)
    BladeType = models.CharField(max_length=100)
    BladeID = models.CharField(max_length=100)
    CoilID = models.CharField(max_length=100)
    BatchNumber = models.CharField(max_length=100)
    SupplierName = models.CharField(max_length=100)
    FiberDetails = models.CharField(max_length=100)
    ShiftDetails = models.CharField(max_length=100)
    Operator = models.CharField(max_length=100)
    Date = models.CharField(max_length=100)
    Time = models.CharField(max_length=100)
    Length = models.CharField(max_length=100)
    class Meta:
        db_table = "metadata"


class MeasuresData(models.Model):   
    ID = models.BigIntegerField()
    BladeType = models.CharField(max_length=100)
    TopWidth_LDL = models.CharField(max_length=100)
    TopWidth_UDL = models.CharField(max_length=100)
    BottomWidth_LDL = models.CharField(max_length=100)
    BottomWidth_UDL = models.CharField(max_length=100)
    TopChamferWidthLeft_LDL = models.CharField(max_length=100)
    TopChamferWidthLeft_UDL = models.CharField(max_length=100)
    TopChamferWidthRight_LDL = models.CharField(max_length=100)
    TopChamferWidthRight_UDL = models.CharField(max_length=100)
    BottomChamferWidthLeft_LDL = models.CharField(max_length=100)
    BottomChamferWidthLeft_UDL = models.CharField(max_length=100)
    BottomChamferWidthRight_LDL = models.CharField(max_length=100)
    BottomChamferWidthRight_UDL = models.CharField(max_length=100)
    ThicknessLeft_LDL = models.CharField(max_length=100)
    ThicknessLeft_UDL = models.CharField(max_length=100)
    ThicknessRight_LDL = models.CharField(max_length=100)
    ThicknessRight_UDL = models.CharField(max_length=100)
    class Meta:
        db_table = "measure_limits"



#main Table
def getPlankDataModel(dbTable):
    class PlankData(models.Model):  
        ID = models.BigIntegerField()
        TCWL = models.CharField(max_length=100)
        TCWR = models.CharField(max_length=100)
        BCWL = models.CharField(max_length=100)
        BCWR = models.CharField(max_length=100)
        ThicknessLeft = models.CharField(max_length=100)
        TopWidth = models.CharField(max_length=100)
        BottomWidth = models.CharField(max_length=100)
        ThicknessRight = models.CharField(max_length=100)
        class Meta:
            db_table = dbTable
    
    return PlankData
    

class SearchForm(forms.Form):
   mode = forms.CharField(max_length = 100)
   bladeId = forms.CharField(max_length = 100)
   coilId = forms.CharField(max_length = 100)
   batchNumber = forms.CharField(max_length = 100)
   operator = forms.CharField(max_length = 100)
   date = forms.DateField()