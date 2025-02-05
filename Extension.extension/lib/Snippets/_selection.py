# -*- coding: utf-8 -*-

#IMPORTS
from Autodesk.Revit.DB import *
from pyrevit import forms


#VARIABLES
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

#FUNCTIONS

def get_selected_elements(uidoc):
    selection = uidoc.Selection.GetElementIds()
    if not selection:
        forms.alert("Выберите элементы перед запуском!", exitscript=True)
    return selection