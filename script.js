
function scroll(){
	dh=document.body.scrollHeight; 
	ch=document.body.clientHeight; 
	if(dh>ch){ 
	moveme=dh-ch
	window.scrollTo(0,moveme)

	} }


function appendMessage(text){ 
	
	a=document.body.scrollHeight; 
	b=document.body.clientHeight;
	c = document.body.scrollTop;
	var insert = document.getElementById('insert')

	var body= document.getElementsByTagName('body')[0]; 
	
	var newline= document.createElement('font'); 
	newline.setAttribute('size','-3'); 
	text=text.replace(/&#34;/g,"\"");
	newline.innerHTML=text; 
	body.appendChild(newline); 

	if (a-b==c){
	 scroll()}}
	 
function appendNextMessage(text){ 
	
	a=document.body.scrollHeight; 
	b=document.body.clientHeight;
	c = document.body.scrollTop;
	var insert = document.getElementById('insert')

	var body= document.getElementsByTagName('body')[0]; 
	
	var newline= document.createElement('font'); 
	newline.setAttribute('size','-3'); 
	text=text.replace(/&#34;/g,"\"");
	newline.innerHTML=text; 
	body.appendChild(newline); 

	if (a-b==c){
	 scroll()}}
