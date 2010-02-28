
import _importer
from gtkmvc import Model

class PosModel (Model):
    posx,posy=(0,0)
    sizex,sizey=(0,0)

    def __init__(self):
        Model.__init__(self)
    def get_pos(self):
        
        return self.posx,self.posy
    
    def set_pos(self,posx,posy):
        self.posy=posy
        self.posx=posx
    def set_size(self,sizex,sizey):
        
        self.sizex=sizex
        self.sizey=sizey