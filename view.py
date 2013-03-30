import wpf
import clr

clr.AddReference("System")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")

from System.Windows import Application, Window
from System import Windows, Array
from System.Windows import Controls
from System.Collections import ObjectModel
from System.Windows import Forms


class BackupView():
    def __init__(self, index, name, date):
        self.SaveIndex = index
        self.SaveName = str(name)
        self.SaveDate = str(date)

    def __repr__(self):
        return "SaveIndex : " + str(self.SaveIndex) \
             + " SaveName : " + self.SaveName  \
             + " SaveDate : " + self.SaveDate

    ToString=__repr__

class WindowAdd(Window):
    def __init__(self, model):
        self.model = model
        wpf.LoadComponent(self, 'Interfaces\window_add.xaml')

    def onButtonSaveClick(self, sender, e):
        if self.edit:

            self.model.save(self.textBoxSaveName.Text)
            Forms.MessageBox.Show("La sauvegarde de la solution est terminée",
                            "Information", Forms.MessageBoxButtons.OK,
                            Forms.MessageBoxIcon.Information)

            self.Hide()

        else:
            if not self.model.new(self.textBoxSaveName.Text):

                Forms.MessageBox.Show("La sauvegarde de la solution est terminée",
                              "Information", Forms.MessageBoxButtons.OK,
                              Forms.MessageBoxIcon.Information)

                self.Hide()
            else:
                Forms.MessageBox.Show("Erreur !\n" + \
                                        "Ce nom de sauvegarde est déjà utilisé,\n"+
                                        "merci d'en choisir un nouveau",
                                        "Erreur !",
                                        Forms.MessageBoxButtons.OK,
                                        Forms.MessageBoxIcon.Error)

                self.textBoxSaveName.Text = ""
                self.onTextNameChange(self.textBoxSaveName,e)

    def onButtonCancelClick(self, sender, e):
        self.Hide()

    def onTextNameChange(self, sender, e):
        if sender.Text == "":
            self.buttonSave.IsEnabled = False
        else:
            self.buttonSave.IsEnabled = True

    def onWindowAddClose(self, sender, e):
        e.Cancel = True
        self.Hide()

    def ShowDialog(self, filename=None):
        if filename:
            self.buttonSave.IsEnabled = True
            self.textBoxSaveName.Text = filename
            self.textBoxSaveName.IsEnabled = False
            self.edit = True
        else:
            self.buttonSave.IsEnabled = False
            self.textBoxSaveName.Text = ""
            self.textBoxSaveName.IsEnabled = True
            self.edit = False

        Window.ShowDialog(self)

class View(Window):
    def __init__(self, model):
        self.model = model
        self.lastSelected = None
        wpf.LoadComponent(self, 'Interfaces\main.xaml')

        self.window_add = WindowAdd(model)
        self.load_list()

    def listview_SelectionChanged(self, sender, e):
        if self.listview.SelectedItem:
            #Windows.MessageBox.Show(self.listview.SelectedItem.ToString()) # DEBUG
            self.lastSelected = self.listview.SelectedItem
            self.buttonEdit.IsEnabled = True
            self.buttonApply.IsEnabled = True
            self.buttonDelete.IsEnabled = True

        else:
            self.lastSelected = None
            self.buttonEdit.IsEnabled = False
            self.buttonApply.IsEnabled = False
            self.buttonDelete.IsEnabled = False

    def onButtonQuitClick(self, sender, e):
        self.Close()

    def onButtonOpenClick(self, sender, e):
        self.model.open()

    def onMainClose(self, sender, e):
        self.model.Close()

    def onButtonResetClick(self, sender, e):

        result = Forms.MessageBox.Show("Voulez-vous vraiment Réinitialiser la solution ?\n" + 
                                       "Toutes vos données seront perdues !",
                                       "Attention !",
                                       Forms.MessageBoxButtons.OKCancel,
                                       Forms.MessageBoxIcon.Warning,
                                       Forms.MessageBoxDefaultButton.Button2)

        if result == Forms.DialogResult.OK:
            self.model.reset()

            Forms.MessageBox.Show("La remise à Zero de la solution est terminée",
                                  "Information", Forms.MessageBoxButtons.OK,
                                  Forms.MessageBoxIcon.Information)

    def onButtonPurgeClick(self, sender, e):

        result = Forms.MessageBox.Show("Voulez-vous vraiment Purger la solution ?\n" + 
                                       "Tous les documents seront perdues !",
                                       "Attention !",
                                       Forms.MessageBoxButtons.OKCancel,
                                       Forms.MessageBoxIcon.Warning,
                                       Forms.MessageBoxDefaultButton.Button2)

        if result == Forms.DialogResult.OK:

            self.model.purge()

            Forms.MessageBox.Show("La purge des documents de la solution est terminée",
                                  "Information", Forms.MessageBoxButtons.OK,
                                  Forms.MessageBoxIcon.Information)

    def onButtonApplyClick(self, sender, e):

        result = Forms.MessageBox.Show("Voulez-vous vraiment restraurer cette sauvegarde ?\n" + 
                                       "Toutes vos données actuelles eront perdues",
                                       "Attention !",
                                       Forms.MessageBoxButtons.OKCancel,
                                       Forms.MessageBoxIcon.Warning,
                                       Forms.MessageBoxDefaultButton.Button2)

        if result == Forms.DialogResult.OK:

            if self.lastSelected:

                self.model.apply(self.lastSelected.SaveIndex)

                Forms.MessageBox.Show("La restauration de la sauvegarde de la solution est terminée",
                                  "Information", Forms.MessageBoxButtons.OK,
                                  Forms.MessageBoxIcon.Information)
        

    def onButtonListRemoveClick(self, sender, e):
        result = Forms.MessageBox.Show("Voulez-vous vraiment supprimer cette sauvegarde ?\n" + 
                                       "Cette action est irréversible !",
                                       "Attention !",
                                       Forms.MessageBoxButtons.OKCancel,
                                       Forms.MessageBoxIcon.Warning,
                                       Forms.MessageBoxDefaultButton.Button2)

        if result == Forms.DialogResult.OK:
            if self.lastSelected:
                self.model.delete(self.lastSelected.SaveIndex)
            self.load_list()

    def onButtonAddListClick(self, sender, e):
        self.window_add.ShowDialog()
        self.load_list()

    def onButtonEditClick(self, sender, e):
        self.window_add.ShowDialog(self.lastSelected.SaveName)

    def load_list(self):
            self.listview.Items.Clear()
            i = 0
            for bkp in self.model.get_backups():
                item = BackupView(i, bkp.name, bkp.date)     
                self.listview.Items.Add(item)
                i += 1