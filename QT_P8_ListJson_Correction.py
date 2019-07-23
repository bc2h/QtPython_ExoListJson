import sys, json
from PySide2.QtWidgets import (QLabel, QApplication,QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QListWidget, QSpacerItem, QInputDialog)

filename = "repertoire.data"

class Repertoire(QWidget):

    def __init__(self, parent=None):
        super(Repertoire, self).__init__(parent)
        global filename
        self.monRepertoire = {}
        self.labelNom = QLabel("Nom")
        self.labelPrenom = QLabel("Prenom")
        self.labelTel = QLabel("Tel")
        self.leNom = QLineEdit()
        self.lePrenom =  QLineEdit()
        self.leTel = QLineEdit()
        self.lwListeNoms = QListWidget()
        self.pbAjouter = QPushButton("Ajouter")
        self.pbModifier = QPushButton("Modifier")

        self.monRepertoire = self.lireJSON(filename)

        self.lwListeNoms.itemClicked.connect(self.userSelected)
        self.pbAjouter.clicked.connect(self.addUser)
        self.pbModifier.clicked.connect(self.modifyUser)

        layoutLabels = QVBoxLayout()
        layoutLabels.addWidget(self.labelNom)
        layoutLabels.addWidget(self.labelPrenom)
        layoutLabels.addWidget(self.labelTel)

        layoutLineEdit = QVBoxLayout()
        layoutLineEdit.addWidget(self.leNom)
        layoutLineEdit.addWidget(self.lePrenom)
        layoutLineEdit.addWidget(self.leTel)

        HLayout = QHBoxLayout()
        HLayout.addWidget(self.lwListeNoms)
        HLayout.addLayout(layoutLabels)
        HLayout.addLayout(layoutLineEdit)

        HLayoutButtons = QHBoxLayout()
        HLayoutButtons.addSpacerItem(QSpacerItem(100, 10))
        HLayoutButtons.addWidget(self.pbModifier)
        HLayoutButtons.addWidget(self.pbAjouter)

        genLayout = QVBoxLayout()
        genLayout.addLayout(HLayout)
        genLayout.addLayout(HLayoutButtons)

        self.setLayout(genLayout)
        self.updateListw()

    def updateListw(self):
        self.lwListeNoms.clear()
        for fiche in self.monRepertoire["repertoire"]:
            self.lwListeNoms.addItem(fiche["nom"])

    def sauveJSON(self, fileName):
        jsonClasse = json.dumps(self.monRepertoire, sort_keys=True, indent=4)
        f = open(fileName, 'w')
        f.write(jsonClasse)
        f.close()

    def addUser(self):
        retour = QInputDialog().getText(self,"Ajout Utilisateur", "Nom:")
        if retour[0] == "":
            return

        fiche = {}
        fiche["nom"] = retour[0]
        fiche["prenom"] = ""
        fiche["tel"] = ""

        self.monRepertoire["repertoire"].append(fiche)
        self.updateListw()
        self.sauveJSON(filename)

    def modifyUser(self):
        rowSelected = self.lwListeNoms.currentRow()
        self.monRepertoire["repertoire"][rowSelected]["nom"] = self.leNom.text()
        self.monRepertoire["repertoire"][rowSelected]["prenom"] = self.lePrenom.text()
        self.monRepertoire["repertoire"][rowSelected]["tel"] = self.leTel.text()
        self.updateListw()
        self.sauveJSON(filename)

    def userSelected(self):
        rowSelected = self.lwListeNoms.currentRow()
        fiche = self.monRepertoire["repertoire"][rowSelected]
        self.leNom.setText(fiche["nom"])
        self.lePrenom.setText(fiche["prenom"])
        self.leTel.setText(fiche["tel"])

    def lireJSON(self,fileName):
        with open(fileName) as json_file:
            dico = json.load(json_file)
            return dico
        return None


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    rep = Repertoire()
    rep.show()
    # Run the main Qt loop
    sys.exit(app.exec_())