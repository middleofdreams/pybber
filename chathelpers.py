def striptext(text):
	text=text.replace('"',"&#34;")
	text=text.replace("'","&#34;")
	text=text.replace("(","&#40;")
	text=text.replace(")","&#41;")
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