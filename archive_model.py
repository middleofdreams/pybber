# -*- coding: utf-8 -*-
import _importer
from gtkmvc import Model
from connection_model import *
from settings_model import *

class ArchiveModel (Model):
    workpath=os.environ['HOME']+"/.pybber/archive"
    open=""
    archiveclose=observable.Signal()
    __observables__ = ('open','archiveclose')
    def is_created(self,recipent,day):
        path=self.workpath+"/"+recipent
        filepath=path+"/"+day
     
        if not os.path.isdir(self.workpath):
            os.makedirs(self.workpath)
        if not os.path.isdir(path):
            os.makedirs(path)
            f = open(filepath+".html", "w")
            f.write("<html><title>Rozmowa z "+recipent+" z "+day+"</title><meta http-equiv='content-type' content='text/html; charset=UTF-8'></head><body>") 
            f.close()
            f = open(filepath+".txt", "w")
            f.close()
    def archive_append(self,recipent,message,day):
        day=day.replace(" ","-")
     
        self.is_created(recipent,day)
        path=self.workpath+"/"+recipent
        filepath=path+"/"+day
        message="<font size=-3>"+message+"</font>"
        f = open(filepath+".html", "a")
        f.write(message+"<br/>")       
        f.close()
        import re
        p = re.compile(r'<.*?>')
        message= p.sub('|', message)
        f = open(filepath+".txt", "a")
        f.write(message+"\n")       
        f.close()
    def loadlast(self,recipent):
        import datetime
        now=datetime.datetime.now()
        day=now.strftime("%d-%m-%Y")
        path=self.workpath+"/"+recipent
        filepath=path+"/"+day+".html"
        try:
            f = open(filepath, "r")
            text=f.read()
            text=text.split("<br/>")
            html=""
            if len(text)>10:
                i=len(text)-5
                while not text[i].startswith("<font size=-3>"):
                    i=i-1
     
                for y in range(i,len(text)):
                    html=html+text[y]+"<br/>"
            else: 
                for i in text: html=html+i+"<br/>"
            html=html.rstrip("<br/>")+"<hr>"
     
        except:
     
            html=""
        from chathelpers import striptext
        print html
        return html
     
            #while 
    def get_list(self,recipent):
        path=self.workpath+"/"+recipent
        try:
            days=os.listdir(path)
        except:
            days=['Brak rozmￃﾳw']
        days.sort(reverse=True)
        self.open=recipent
        return days
    
    def get_html(self,day,recipent):
        if day==None or day=="Brak rozmￃﾳw": 
            html="<center> Brak rozmￃﾳw w archiwum"
        else: 
            path=self.workpath+"/"+recipent
            filepath=path+"/"+day
            f = open(filepath, "r")
            html=f.read()
            f.close()
            html=html.replace(chr(13),"<br/>")
            html=html.replace("\n","<br/>")
            #if not "<font size=-3>"
        return html


    