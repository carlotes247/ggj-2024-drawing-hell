import json
import random

class DialogueState:

    def __init__(self, file, dialogue):
        
        with open(file, "r")  as f:
            data = json.load(file)
            
            self.accept = data["acceptResponse"]
            self.reject = data["rejectResponse"]
            self.request = data["request"]
        
        self.diag = dialogue
        
        sef.currRequest = None
        
        
    
    def accept(self):
        self.currRequest = None
        acc = random.choice(self.accept)
        #parse response
        self.diag.setText(acc["acceptText"])
    
    def reject(self):
        self.currRequest = None
        acc = random.choice(self.reject)
        #parse response
        self.diag.setText(acc["rejectText"])
    
    def request(self):
        req = random.choice(self.request)
        self.currRequest = req
        self.dia.setText(req["requestText"])
    
    def checkResponse(self):
        self.accept()
        