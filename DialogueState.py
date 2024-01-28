import json
import random

class DialogueState:
    def __init__(self, file, dialogue):
        
        with open(file, "r")  as f:
            data = json.load(f)
            
            self.acceptTxt = data["acceptResponse"]
            self.rejectTxt = data["rejectResponse"]
            self.requestTxt = data["request"]
        
        self.diag = dialogue
        
        self.currRequest = None
    
    def accept(self):
        self.currRequest = None
        acc = random.choice(self.acceptTxt)
        #parse response
        self.diag.setText(acc["acceptText"])
    
    def reject(self):
        self.currRequest = None
        acc = random.choice(self.rejectTxt)
        #parse response
        self.diag.setText(acc["rejectText"])
    
    def request(self):
        req = random.choice(self.requestTxt)
        self.currRequest = req
        self.diag.setText(req["requestText"])
    
    def checkResponse(self):
        self.accept()
        