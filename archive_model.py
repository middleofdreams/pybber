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
    def archive_append(self,time,name,msg,day,recipent,message,out=False):
        day=day.replace(" ","-")
        if out: name="!ME!"
        self.is_created(recipent,day)
        path=self.workpath+"/"+recipent
        filepath=path+"/"+day
        message="<font size=-3>"+message+"</font>"
        f = open(filepath+".html", "a")
        f.write(message+"<br/>")       
        f.close()
        text=time+"|"+name+"|"+msg
        f = open(filepath+".txt", "a")
        f.write(text+"\n")       
        f.close()
    def loadlast(self,recipent,style,me):
        import datetime
        now=datetime.datetime.now()
        day=now.strftime("%d-%m-%Y")
        path=self.workpath+"/"+recipent
        filepath=path+"/"+day+".txt"
        try:
            f = open(filepath, "r")
            text=f.read()
            text=text.split("\n")
            html=""
            last=""
            if len(text)>15:
                i=len(text)-10
            else:
                i=len(text)
            from chathelpers import set_archstyle
            for y in range(i,len(text)-1):
                line=text[y].split("|")
                print line
                if line[1]==last: continous=True
                else: continous=False
                last=line[1]
                if line[1]=="!ME!":
                    outgoing=True
                    
                    line[1]=me
                    
                else: outgoing=False
                html=html+set_archstyle(line[0],line[1],line[2],outgoing=outgoing,continous=continous,style=style)

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


    