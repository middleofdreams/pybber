def striptext(text,br=True,ss=True):
	text=text.replace('"',"&#34;")
	text=text.replace("'","&#39;")
	if ss:
		text=text.replace("(","&#40;")
		text=text.replace(")","&#41;")
	if br:
		text=text.replace(chr(13),"<br/>")
		text=text.replace("\n","<br/>")
	return text

def intolink(urlstr):
	import re
	pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	pat2 = re.compile(r"(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", re.IGNORECASE | re.DOTALL)
	urlstr = pat1.sub(r'\1<a href="\2" target="_blank" title="\2">\3</a>', urlstr)
	urlstr = pat2.sub(r'\1<a href="http://\2" target="_blank" title="\2">\3</a>', urlstr)
	
	return urlstr
def messtime(ts):
	import time
	tp=time.mktime(time.strptime(ts,'%Y%m%dT%H:%M:%S'))+3600
	if time.localtime()[-1]: tp+=3600
	tp=time.localtime(tp)	
	tm=time.strftime("%H:%M:%S",tp)
	day=time.strftime("%d %m %Y",tp)
	return tm,day

def showimages(text):
	text=text.replace("[img:","<img src=\"")
	text=text.replace(".bmp]",".bmp\">")
	text=text.replace(".jpg]",".jpg\">")
	text=text.replace(".png]",".png\">")
	text=text.replace(".jpeg]",".jpeg\">")
	text=text.replace(".gif]",".gif\">")
	return text

def set_style(time,who,message,outgoing=True,continous=False,style="default"):
	if style=="default":
		if outgoing:
			text="<i>("+time+")</i><b> <font color=blue>"+who+"</font></b>: "+message
		else:
			text="<i>("+time+")</i><b> <font color=red>" \
								+who+"</font></b>: "+message
	else:
		if outgoing:
			if continous:
				path='chatstyles/'+style+'/Outgoing/NextContent.html'
				apath='chatstyles/'+style+'/Outgoing/NextContext.html'
			else:
				path='chatstyles/'+style+'/Outgoing/Content.html'
				apath='chatstyles/'+style+'/Outgoing/Context.html'
			f=open(path)
			text=f.read()
			f.close
			f=open(apath)
			archive=f.read()
			f.close
			text=text.replace("%userIconPath%","chatstyles/out_icon.png")
			archive=archive.replace("%userIconPath%","chatstyles/out_icon.png")

		else:  
			if continous:
				path='chatstyles/'+style+'/Incoming/NextContent.html'
				apath='chatstyles/'+style+'/Incoming/NextContext.html'
			else:
				path='chatstyles/'+style+'/Incoming/Content.html'
				apath='chatstyles/'+style+'/Incoming/Context.html'
			f=open(path)		
			text=f.read()
			f.close
			f=open(apath)
			archive=f.read()
			f.close
			text=text.replace("%userIconPath%","chatstyles/in_icon.png")
			archive=archive.replace("%userIconPath%","chatstyles/in_icon.png")

		
		text=changetext(text,time,who,message)
		archive=changetext(archive,time,who,message)
	return text,archive

def changetext(text,time,who,message):
	text=striptext(text,False,False)
	text=text.replace("\n","")
	text=text.replace("%sender%",str(who))
	text=text.replace("%message%",message)
	ltime=time.split(":")
	ltime=ltime[0]+":"+ltime[1]
	text=text.replace("%time{%H:%M}%",ltime)
	text=text.replace("%time{%H:%M:%S}%",time)
	text=text.replace("%time%",time)
	text=text.replace("%service%",'')
	return text

def set_archstyle(time,who,message,outgoing=True,continous=False,style="default"):
	if style=="default":
		if outgoing:
			text="<i>("+time+")</i><b> <font color=blue>"+who+"</font></b>: "+message
		else:
			text="<i>("+time+")</i><b> <font color=red>" \
								+who+"</font></b>: "+message
	else:
		if outgoing:
			if continous:
				path='chatstyles/'+style+'/Outgoing/ANextContext.html'
			else:
				path='chatstyles/'+style+'/Outgoing/AContext.html'
			f=open(path)
			text=f.read()
			f.close
			
			text=text.replace("%userIconPath%","chatstyles/out_icon.png")


		else:  
			if continous:
				path='chatstyles/'+style+'/Incoming/ANextContext.html'
			else:
				path='chatstyles/'+style+'/Incoming/AContext.html'
			f=open(path)		
			text=f.read()
			f.close			
			text=text.replace("%userIconPath%","chatstyles/in_icon.png")

		
		text=changetext(text,time,who,message)
	return text