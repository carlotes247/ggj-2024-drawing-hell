import json
import random
import torch
from ModelTorch import *
from ModelLoader import *
from ModelEvaluator import *



class DialogueState:
    def __init__(self, file, dialogue):
        
        with open(file, "r")  as f:
            data = json.load(f)
            
            self.acceptTxt = data["acceptResponse"]
            self.rejectTxt = data["rejectResponse"]
            self.requestTxt = data["request"]
        
        self.diag = dialogue
        
        self.currRequest = None
    
    def accept(self, obj):
        acc = random.choice(self.acceptTxt)
        txt = acc["acceptText"]
        #parse response
        if ("expObjName" in acc.keys()):
            txt = txt.replace(acc["expObjName"], self.currRequest["objType"])
        if ("acqObjName" in acc.keys()):
            txt = txt.replace(acc["acqObjName"], obj)
        self.diag.setText(txt)
        self.currRequest = None
    
    def reject(self, obj):
        acc = random.choice(self.rejectTxt)
        txt = acc["rejectText"]
        #parse response
        if ("expObjName" in acc.keys()):
            txt = txt.replace(acc["expObjName"], self.currRequest["objType"])
        if ("acqObjName" in acc.keys()):
            txt = txt.replace(acc["acqObjName"], obj)
        self.diag.setText(txt)
        self.currRequest = None
    
    def request(self):
        req = random.choice(self.requestTxt)
        self.currRequest = req
        self.diag.setText(req["requestText"])
    
    def checkResponse(self, image, model, device):
        predictedClass = Classify(model, device, classes, test_data, image)
        if (predictedClass == self.currRequest["objType"]):
            self.accept(predictedClass)
        else:
            self.reject(predictedClass)
        