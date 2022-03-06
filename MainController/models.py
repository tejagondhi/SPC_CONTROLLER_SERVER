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

#main Table
def getPlankDataModel(dbTable):
    class PlankData(models.Model):  
        ID = models.BigIntegerField()
        TCWL = models.CharField(max_length=100)
        TCWR = models.CharField(max_length=100)
        BCWL = models.CharField(max_length=100)
        BCWR = models.CharField(max_length=100)
        TotalThickness = models.CharField(max_length=100)
        TopTotalWidth = models.CharField(max_length=100)
        BottomTotalWidth = models.CharField(max_length=100)
        FinalTotalWidth = models.CharField(max_length=100)
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