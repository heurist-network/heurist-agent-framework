from enum import Enum
class Phase(Enum): SPROUT="sprout"; GREEN="green_leaf"; YELLOW="yellow_leaf"; RED="red_leaf"; SOIL="soil"
class CapsuleTracker:
    def __init__(self): self.d={}
    def add(self,i,c,p="P2"): self.d[i]={'c':c,'p':p,'conf':0.7,'phase':Phase.SPROUT}
    def access(self,i):
        if i in self.d: self.d[i]['conf']=min(1.0,self.d[i]['conf']+0.03); self.d[i]['phase']=Phase.GREEN if self.d[i]['conf']>=0.8 else Phase.SPROUT; return True
        return False
