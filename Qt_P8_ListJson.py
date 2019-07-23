import sys, json
from PySide2.QtWidgets import (QLabel, QApplication,QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QListWidget, QSpacerItem, QInputDialog, QSizePolicy)
from ui_Qt_P8_ListJson_Design import Ui_Form #nom de la classe générée


filename = "listeContact.json"  #liste de dictionnaires

class Repertoire(QWidget):

    def __init__(self, parent=None):
        super(Repertoire, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # permet de charger tous les composants graphiques coder dans un autre fichier
    # partir du fichier .py (au lieu du .ui) permet d'accéder à la complétion cad la liste des fonctions, widgets...

        global filename
        self.monRepertoire = self.lireJSON(filename)

        self.ui.pbAjout.clicked.connect(self.ajoutContact)
        self.ui.pbModif.clicked.connect(self.modifContact)
        self.ui.listNom.itemClicked.connect(self.selectContact)


    def ajoutContact(self):  #ajout d'un dictionnaire à la liste de dico
        retour = QInputDialog().getText(self, "Ajout Contact", "Nom:") #ouverture d'une nouvelle fenetre pour créer un contact
        if retour[0] == "":
            return
        else:
            fiche = {}
            fiche["nom"] = retour[0]
            fiche["prenom"] = ""
            fiche["tel"] = ""
            self.monRepertoire["repertoire"].append(fiche) #ajout du dicco à la liste de dico
            self.majListeContact()

            self.sauveJSON(filename)

    def modifContact(self):
        rowSelected= self.ui.listNom.currentRow()
        self.monRepertoire["repertoire"][rowSelected]["nom"] = self.ui.ledNom.text()
        self.monRepertoire["repertoire"][rowSelected]["prenom"] = self.ui.ledPrenom.text()
        self.monRepertoire["repertoire"][rowSelected]["tel"] = self.ui.ledTel.text()
        self.majListeContact()
        self.sauveJSON(filename)

    def selectContact(self):
        rowSelected = self.ui.listNom.currentRow()
        fiche = self.monRepertoire["repertoire"][rowSelected]
        self.ui.ledNom.setText(fiche["nom"])
        self.ui.ledPrenom.setText(fiche["prenom"])
        self.ui.ledTel.setText(fiche["tel"])

    def majListeContact(self):
        self.ui.listNom.clear()
        for fiche in self.monRepertoire["repertoire"]:
            self.ui.listNom.addItem(fiche["nom"])

    def lireJSON(self,fileName):
        with open(fileName) as json_file:
            dico = json.load(json_file)
            return dico
        return None

    def sauveJSON(self, fileName):
        pass
        # jsonClasse = json.dumps(self.monRepertoire, sort_keys=True, indent=4)
        # f= open(fileName, 'w')
        # f.write(jsonClasse)
        # f.close()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    rep = Repertoire()
    rep.show()
    # Run the main Qt loop
    sys.exit(app.exec_())