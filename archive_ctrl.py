import _importer
from gtkmvc import Controller
from gtkmvc.adapters import Adapter

class ArchiveCtrl (Controller):
    
    def register_view(self,view):
        view.archive_create()
    
    def archive(self,widget):
        self.view.archive_show()
        index=self.view['list'].get_selection()
        index=index.get_selected()[1]
        recipent=self.view['listmodel'].get_value(index,4)
        days=self.model.get_list(recipent)
        for day in days:
            day=day.rstrip('.txt')
            self.view.archive_addtolist(day,recipent)
           
        html=self.model.get_html(days[0],recipent,"Ja")
        self.view.archive_showchat(html)   
        self.view['window'].set_title("Archiwum rozmowy z "+recipent)
    def loadarchive(self,widget, row, col):
        model = widget.get_model()
        day = model[row][0]
        day=day+".txt"
        recipent=model[row][1]
        html=self.model.get_html(day,recipent,"Ja")
        self.view.archive_showchat(html)
        
    def closearchive(self,widget):
        self.view.archive_close()
        
        self.model.archiveclose.emit(self.model.open)
        self.model.open=""
