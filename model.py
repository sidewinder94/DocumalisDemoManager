# -*- coding: utf-8 -*-
import ConfigParser
import clr
import re
import shutil
import zipfile
import time
import os

clr.AddReference("mscorlib")
clr.AddReference("System.Data")
clr.AddReference("System.Windows.Forms")
clr.AddReference("WindowsBase")
clr.AddReference("System.ServiceProcess")

from System.IO import Packaging
from System import IO, Convert, Windows, Security, Data, String, Uri, UriKind, \
                   Byte, Array, DateTime, Diagnostics, ServiceProcess, \
                   InvalidOperationException, Version
from os.path import basename
from System.Text import RegularExpressions
from System.Windows.Forms import MessageBox #DEBUG

INIFILE = ".\\config.ini"
BUFFER_SIZE = 4096
BASE_SAVE_DIR = ".\\Backups"

#Classe permettant le chargement d'un fichier ini en tant que dictionnaire 
#à double entrée
class IniParser(ConfigParser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

#Classe de gestion des sauvegardes
class Backup:
    def __init__(self, name, file, date, database):
        #Définition des propriétés de la sauvegarde
        self.name = name
        self.file = file
        self.date = date
        self.database = database

    #Restauration de la sauvegarde
    def apply(self, installdir, temp_dir="C:\\Temp", sup_files=[]):
        #On vide le dossier temporaire
        if  IO.Directory.Exists(temp_dir):
            IO.Directory.Delete(temp_dir, True)

        #On extrait la sauvegarde
        self.extract_zip(self.file, temp_dir)

        #On restaure les documents dans Datadoc en ayant préalablement supprimé les dossiers s'y rouvant si existants
        if IO.Directory.Exists(temp_dir + "\\Datadoc"):
            for document_dir in IO.Directory.GetDirectories(temp_dir +" \\Datadoc"):
                dirname = re.sub("^.+\\\\","",document_dir)
                IO.Directory.Delete(installdir + "\\" + dirname , True)
                shutil.copytree(document_dir, installdir + "\\" + dirname )

        #On copie les fichiers copiés supplémentaires dans l'arborescence en écrasant
        installdir = re.sub(r"\\[^\\]+$","", installdir)
        self.multiple_copy(temp_dir, installdir, sup_files)

        #On Restaure les bases de données SQL
        self.database.restore_all(temp_dir + "\\Databases")

        #On nettoie le dossier temp
        self.temp_clean_nodebug()

    #Fonction permettant la sauvegarde dans un zip nommé placé dans le répertoire "Backups"
    #Le paramètre temp_dir peut provoquer des erreurs si contient des espaces
    #Erreur sur un partage ou lecteur réseau
    def save(self, installdir, destdir,temp_dir="C:\\Temp", sup_files=[]):
        #Verification de l'existance des dossiers nécessaires et de leur contenu 
        #ainsi que de la non existance du zip de destination
        if not IO.Directory.Exists(destdir):
            IO.Directory.CreateDirectory(destdir)

        if  IO.Directory.Exists(temp_dir):
            IO.Directory.Delete(temp_dir, True)

        if IO.File.Exists(destdir + "\\" + self.name + ".zip"):
            IO.File.Delete(destdir + "\\" + self.name + ".zip")

        #Création des dossiers temporaires
        IO.Directory.CreateDirectory(temp_dir)
        IO.Directory.CreateDirectory(temp_dir + "\\Databases")

        #On ajoute l'utlisateur Service Réseau un accès complet au dossier temporaire
        self.folder_rights(temp_dir, "SERVICE RÉSEAU")
        self.folder_rights(temp_dir, "Tout le monde")

        #On lance le backup des bases de données
        self.database.backup_all(temp_dir + "\\Databases")

        #On copie les documents
        shutil.copytree(installdir,temp_dir + "\\Datadoc",True,None)

        #On Ajoute les fichiers supplémentaires
        installdir = re.sub(r"\\[^\\]+$","", installdir)
        self.multiple_copy(installdir, temp_dir, sup_files)
        
        #On Zippe le contenu du dossier temporaire
        files = IO.Directory.GetFiles(temp_dir, "*", 
                                      IO.SearchOption.AllDirectories)

        for file in files:
            self.add_file_zip(destdir + "\\" + self.name + ".zip", 
                              temp_dir,file)

        #On s'assure que le nom de la sauvegarde est correcte (pour affichage)
        self.name = destdir.replace(BASE_SAVE_DIR,"") + "\\" + self.name + ".zip"
        self.name = self.name.Trim("\\")

        #Nettoyage du dossier temp
        self.temp_clean_nodebug()

    #Fonction permettant de copier les fichiers correspondant à un masque
    #en conservant l'arborescence
    #Chaque ligne de la liste masks doit être construite ainsi : <chemin>|<masque>[|recursive]
    #Où <chemin> est le chemin relatif d'accès au répertoire à copier depuis source_dir
    #Où <masque> est un masque permettant de filtrer les fichiers copiés
    #Où recursive est un paramètre optionnel définissant par sa présence une recherche récursive
    def multiple_copy(self,source_dir,dest_dir, masks):
        #On crée un fichier de log
        log = IO.File.CreateText(".\\Logs\\CopyFilesLog_" + \
                                 str(time.strftime("%d-%m-%Y %H-%M-%S",time.localtime())) +\
                                 ".log")

        #On liste tous les fichiers supplémentaires
        for key, filter in masks.items():
            #On sépare les valeurs contenues dans l'item de la liste
            tab = filter.Split("|")
            try:
                found = []
                search = IO.SearchOption.TopDirectoryOnly
                #Si on trouve moins de 2 items la chaine n'est pas correcte
                if len(tab) < 2:
                    continue
                #Si on trouve plus de 2 items on vérifie si le troisième est "recursive"
                elif len(tab) > 2:
                    #Si le troisieme item correspond a "recursive" la recherche sera récursive
                    if tab[2] == "recursive":
                        search = IO.SearchOption.AllDirectories
                    found = IO.Directory.GetFiles(source_dir + "\\Distrib\\" + tab[0], 
                                                  tab[1], search)
                    log.WriteLine("Copie de " + tab[0] + " commencée avec le filtre " + tab[1])
                #Si on trouve exactement 2 items on lance la recherche non récursive
                else:
                    found = IO.Directory.GetFiles(source_dir + "\\Distrib\\" + tab[0], tab[1], search)
                    log.WriteLine("Copie de " + tab[0] + " commencée avec le filtre " + tab[1])
                

                #On Copie dans le dossier Distrib de temp
                for file in found:
                    dir = re.sub(r"\\[^\\]+$","",file)
                    dir = dir.Replace(source_dir, dest_dir)

                    #Si le sous-répertoire de destination n'existe pas on le crée
                    #avec son arborescence
                    if not IO.Directory.Exists(dir):
                        IO.Directory.CreateDirectory(dir)

                    #On copie le fichier de l'arborescence source à l'arborescence
                    #de destination
                    IO.File.Copy(file,file.Replace(source_dir, dest_dir),True)    

                    #On ecrit dans le log chaque fichier copié
                    log.WriteLine("Copie de : " + file + " dans : " + 
                                  file.Replace(source_dir, dest_dir) + "terminée")

            #Si une exception survient on l'écrit dans le log
            except (Exception) as e:
                log.WriteLine(e)

        #On Ferme le fichier de log
        log.Close()

    #Suppression d'une sauvegarde
    def delete(self):
        #On supprime l'archive contenant la sauvegarde
        IO.File.Delete(self.file)

        #Si le repertoire contenant l'archive est vide, on le supprime
        for dir in IO.Directory.GetDirectories(".\\Backups"):
            if IO.Directory.GetFiles(dir,"*",IO.SearchOption.AllDirectories).Length == 0:
                IO.Directory.Delete(dir, True)
             
    #Nettoyage du dossier temporaire si l'option "purgeafter" de la section "Temp" de l'ini n'est pas définie
    def temp_clean_nodebug(self):
        try:
            #Essaie de récupérer la valeur de l'ini
            execute = Convert.ToInt32(self.database.config.data["Temp"]["purgeafter"])
        except:
            #Si echec de la lecture de la section Debug de l'ini, on purge car
            #on considère ne pas être en mode debug
             execute = True
        finally:
            #Si execute n'as pas la valeur False ou 0, on clean le dossier
            if execute:
                IO.Directory.Delete(self.database.config.data["Temp"]["folder"],True)

    #Fonction permettant si l'utilisateur en a les droits d'attribuer le controle total
    #sur un dossier à un utilisateur donné    
    def folder_rights(self, folder, user):
        dir_security = IO.Directory.GetAccessControl(folder)
        rights = Security.AccessControl.FileSystemRights.FullControl
        rule = Security.AccessControl.FileSystemAccessRule(user,
                                                           rights, 
                                                           Security.AccessControl.InheritanceFlags.ObjectInherit,
                                                           Security.AccessControl.PropagationFlags.None,
                                                           Security.AccessControl.AccessControlType.Allow)
        dir_security.AddAccessRule(rule)
        IO.Directory.SetAccessControl(folder,dir_security)

    #Fonction extrayant "zip_file" dans le repertoire "destdir"
    #L'extraction ne supporte ni la fusion ni l'écrasement
    def extract_zip(self, zip_file, destdir):
        zip = zipfile.ZipFile(zip_file,"r")
        zip.extractall(destdir)
        zip.close()

    #Ajoute "file" a "zip_file", se basant sur "basedir" pour recréer l'arborescence
    #dans le "zip_file"
    def add_file_zip(self, zip_file, basedir, file):
        zip = zipfile.ZipFile(zip_file, "a")
        arch_path = file.replace(basedir + "\\","")
        zip.write(file, arch_path)
        zip.close()

#Classe chargée de charger la configuration depuis un fichier ini ou de le réecrire
#si ce dernier est corrompu
class Config:
    def __init__(self):
        self.file = None

    #Essaie de charger la configuration, si la configuration est nulle,
    #ecrit le fichier de configuration
    def init(self, file, default=None):
        self.file = file
        ini = self.ini_load()
        if not ini:
            self.data = default
            self.ini_write()
        else:
            self.data = ini

    #Tente de charger les données du fichier de configuration, si echec, retourne None
    def ini_load(self):
        try:
            inifile = IniParser()
            inifile.read(self.file)
            return inifile.as_dict()
        except ConfigParser.MissingSectionHeaderError as e:
            return None
    
    #Ecrit la configuration par défaut dans le fichier de configuration
    def ini_write(self):
            #Création du fichier de configuration
            file = IO.File.CreateText(self.file)

            #Écriture des valeurs dans le fichier
            for k,v in self.data.items():
                file.WriteLine("["+k+"]")
                for pk,pv in v.items():
                    file.WriteLine(pk+"="+pv)

            #Fermeture du fichier
            file.Close()

#Principale classe du programme, c'est elle qui se chargera d'effectuer ou de commencer
#la pluapart des actions
class Model:
    def __init__(self):
        self.workingdir = ".\\Backups\\"
        self.ext = "*.zip"
        self.backups = []
        self.database = None
        #On crée un fichier de log
        IO.Directory.CreateDirectory(".\\Logs")
        log = IO.File.CreateText(".\\Logs\\LoadLog_" + \
                                      str(time.strftime("%d-%m-%Y %H-%M-%S",time.localtime())) +\
                                      ".log")
        log.WriteLine("Chargement de la config : ")
        # Charge le fichier de configuration
        # Definition de l'ini par défaut si l'ini de configuration est absent ou invalide
        # La casse est importante pour le nom des sections mais ne l'est pas pour le NOM des clés
        default_ini = {"General":{"installdir":"C:\\Documalis"},
                       "SQL":{"server":"localhost\\SQLEXPRESS",
                              "username":"sa",
                              "password":"newton"},
                       "Bases":{"CONFIG":"1",
                                "DOCUMENT":"1",
                                "COLLECT":"1",
                                "FLOW":"1",
                                "PUBLISH":"1",
                                "RECOGNIZE":"1"},
                       "Temp":{"folder":"C:\\Temp",
                               "purgeafeter":"0"},
                       "Services":{"rootservice":"Doc Recovery Server"},
                       "Files":{"filter1":r"Server\Collect Server\Jobs\Collect|*.workflow",
                                "filter2":r"Server\Collect Server\Jobs\Preprocess|*.workflow",
                                "filter3":r"Server\Flow Server\Jobs\Auto|*.workflow",
                                "filter4":r"Server\Flow Server\Jobs\Flow|*.workflow",
                                "filter5":r"Server\Publish Server\Jobs\Publish|*.workflow",
                                "filter6":r"Server\Config Server\ConfigServer\Data\Flow_Process|Custom.slib",
                                "filter7":r"Server\Config Server\ConfigServer\Data\Flow_Process|Hook.slib",
                                "filter8":r"Server\Recognize|*.*|recursive",
                                "filter9":r"Client\Wizard\AutoPlay\Data\ModelStat|*.*",
                                "filter10":r"Server\Config Server\ConfigServer\Data|Wizard*.zip"}
                      }
        log.Write("Chargement de la config : ")
        self.config = Config()
        self.config.init(INIFILE, default_ini)
        log.WriteLine("OK")
        self.log = IO.File.CreateText(".\\Logs\\ResetLog_" + \
                                      str(time.strftime("%d-%m-%Y %H-%M-%S",time.localtime())) +\
                                      ".log")

        log.Write("Chargement des infos BDD")
        # create database access
        try:
            self.database = Database(self.config)

            for name, activated in self.config.data["Bases"].items():
                if activated:
                    self.database.list.append(name.ToUpper())
            self.temp = self.config.data["Temp"]["folder"]
        except KeyError: #Si une clé est manquante dans l'ini, on restaure la config par défaut
            self.config.data = default_ini
            self.config.ini_write()
            self.config.init(INIFILE, default_ini)
        log.WriteLine(" : OK")
        #Définitions de chemin d'accès
        self.execSQL_path = self.config.data["General"]["installdir"] +\
                       "\\Distrib\\Server\\Common\\ExecSQL.exe"
        self.execSQL_process = Diagnostics.Process

        self.serverdir = self.config.data["General"]["installdir"] +\
                       "\\Distrib\\Server"
        
        self.docsdir = self.config.data["General"]["installdir"] + "\\Datadoc"

        log.Write("Chargement des sauvegardes : ")
        # load backups
        if not IO.Directory.Exists(".\\Backups"):
            IO.Directory.CreateDirectory(".\\Backups")
        files = IO.Directory.GetFiles(self.workingdir, self.ext, 
                                      IO.SearchOption.AllDirectories)

        for file in files:
            name = file.replace(self.workingdir, "")
            date = Convert.ToString(IO.File.GetLastWriteTime(file))
            self.backups.append(Backup(name, file, date, self.database))
        log.Write("OK")
        log.Close()
    #Renvoie la liste des sauvegarde à la vue
    def get_backups(self):
        return self.backups

    #Purge des documents
    def purge(self):
        #Arret des services
        self.services_control(self.config.data["Services"]["rootservice"],False)

        #Vidage de Datadoc
        self.clean_datadoc()

        #Purge des documents dans la base de données
        zcfgs = IO.Directory.GetFiles(self.serverdir, "*.zcfg", IO.SearchOption.AllDirectories)
        for sql in IO.Directory.GetFiles(IO.Directory.GetCurrentDirectory() + "\\SQL"):
            for zcfg in zcfgs:
                sql_cleaned = re.sub("^.+\\\\purge-","", sql)
                sql_cleaned = sql_cleaned.replace(".sql","")
                if zcfg.Contains(sql_cleaned.title() + " " + "Server"):
                    process = self.execSQL_process.Start(self.execSQL_path,'zcfg="' + zcfg + '" sql="' + sql + '"')
                    process.WaitForExit()

        #On nettoie l'arborescence
        self.purge_files()

        #Redémarrage des services
        self.services_control(self.config.data["Services"]["rootservice"],True)

    #Remise à zero de la solution
    def reset(self, mode="reset"):

        #Suppression et recréation des Bases de donnés
        self.database.drop_all()
        self.database.create_all()

        #Arret des services
        self.services_control(self.config.data["Services"]["rootservice"],False)

        #On cherche les fichiers sql et zcfg correspondants et on les execute avec ExecSQL
        for server in IO.Directory.GetDirectories(self.serverdir):
            for zcfg in IO.Directory.GetFiles(server,"*.zcfg",IO.SearchOption.TopDirectoryOnly):  
                for sql in IO.Directory.GetFiles(server,"*.sql",IO.SearchOption.AllDirectories):
                    #On vérifie que les fichiers exécutés sql sont bien les bons (destinés a SQL Server zet seulement les create et insert
                    if sql.ToLower().Contains("sql server") and not sql.ToLower().Contains("update"):    
                        process = self.execSQL_process.Start(self.execSQL_path, 'zcfg="' + zcfg + '" sql="' + sql + '"')
                        process.WaitForExit()
                        if self.execSQL_process.ExitCode:

                            #En cas d'erreur on ecrit dans le log qui annoncera l'emplacement de l'erreur
                            if not IO.Directory.Exists(".\\Logs"):
                                IO.Directory.CreateDirectory(".\\Logs")

                        
                            self.log.WriteLine("Echec de l'exécution du fichier SQL : " +\
                                                sql + "\n utilisant le fichier de configuration : " +\
                                                zcfg)

        #Nettoyage de Datadoc
        self.clean_datadoc()

        #Nettoyage de l'arborescence
        self.purge_files()

        if mode == "reset":
            #Redémarrage des services
            self.services_control(self.config.data["Services"]["rootservice"],True)
    
    #TODO : Gérer les exceptions concernant des nom de services inexistants ou des servies impossibles à démarrer
    #Idées : Fichier de Log
    def services_control(self, service, state):
        control = ServiceProcess.ServiceController(service, ".")
        if state:
            if not control.Status == ServiceProcess.ServiceControllerStatus.Running:
                try:
                    control.Start()
                except InvalidOperationException as e:
                    MessageBox.Show("Erreur de démarrage du service : " + service)
        else:
            if control.CanStop:
                try:
                    control.Stop()
                except InvalidOperationException as e:
                    MessageBox.Show("Erreur de l'arret du service : " + service)

    def clean_datadoc(self):
        #Suppression des fichiers et dossiers contenus dans Datadoc
        for dir in IO.Directory.GetDirectories(self.docsdir):
            for file in IO.Directory.GetFiles(dir):
                IO.File.Delete(file)
            for directory in IO.Directory.GetDirectories(dir):
                IO.Directory.Delete(directory,True)

    #Actions à effectuer à la fermeture de l'application
    def Close(self):
        self.log.Close()
        for log in IO.Directory.GetFiles(".\\Logs"):
            if IO.File.ReadAllLines(log).Length == 0:
                IO.File.Delete(log)

    #Retourne l'index de la position à laquelle a été trouvé la sauvegarde nommée, -1 si non trouvée
    def find_backup(self, name):
        i = 0
        found = False
        for backup in self.backups:
            if backup.name in [name, name+".zip"]:
                found = True
                break
            i += 1

        if found:
            return i
        else:
            return -1 

    #Modification d'une sauvegarde existante
    def save(self, name):
        i = self.find_backup(name)

        if i >= 0:
            self.backups[i].name = name.replace(".zip","")
            self.backups[i].date = DateTime.Now
            self.backups[i].save(self.config.data["General"]["installdir"]+"\\Datadoc",
                                 BASE_SAVE_DIR, self.temp, self.config.data["Files"])

    #Retourne True si erreur et False si non
    #Fonction permettant de créer une nouvelle sauvegarde
    def new(self, name):
        date = DateTime.Now
        
        path = BASE_SAVE_DIR

        if (name.Contains("\\")):
            found = re.sub("\\\\\\w+$", "", name)
            path += "\\" + found
            filename = name.replace(found + "\\","")

        else:
            filename = name

        if self.find_backup(name) >= 0:
            return True

        bkp = Backup(filename, path + "\\" + filename + ".zip", date, self.database)
        self.backups.append(bkp)
        bkp.save(self.config.data["General"]["installdir"]+"\\Datadoc", 
                                  path,self.temp, self.config.data["Files"])
        return False

    #Application d'une sauvegarde
    def apply(self, index):
        try:
            #On stoppe les services
            self.services_control(self.config.data["Services"]["rootservice"],False)

            #On nettoie le dossier de l'application
            self.purge_files()

            #On commence la restauration
            self.backups[index].apply(self.config.data["General"]["installdir"]+"\\Datadoc", self.temp,
                                      self.config.data["Files"])

            #On applique les mises à jour
            self.apply_updates()

            #Redémarrage des services
            self.services_control(self.config.data["Services"]["rootservice"],True)

        except(IndexError):
            pass
    
    #Appel des batchs de purge des fichiers de la solution
    def purge_files(self):
        bat_path = self.config.data["General"]["installdir"] + r"\Distrib\purge.bat"
        for batch in IO.Directory.GetFiles(r".\Scripts","*.bat",
                                           IO.SearchOption.TopDirectoryOnly):
            IO.File.Copy(batch, bat_path,True)
            os.system(bat_path)
            IO.File.Delete(bat_path)

    #TODO : Finir cette fonction
    def apply_updates(self):
        #Création d'un log
        log = IO.File.CreateText(".\\Logs\\UpdatesLog_" + \
                                      str(time.strftime("%d-%m-%Y %H-%M-%S",time.localtime())))

        installdir = self.config.data["General"]["installdir"] + "\\Distrib"
        #On applique les updates pour toutes les bases de données
        for server in IO.Directory.GetDirectories(installdir):
            # récupérer les fichiers
            list = []
            for update in IO.Directory.GetFiles(server, "update-*.sql", IO.SearchOption.AllDirectories):
                if update.ToLower().Contains("sql server"):
                    list.append(update)
            
            # trier par numéro de version
            list = sorted(list, 
                   cmp = lambda x, y:  1 if x > y else 0 if x == y else -1,
                   key = lambda path: Version(re.sub("^.+\\\\update-", "", path).replace(".sql", "")))

            # appliquer
            for update in list:
                zcfg = IO.Directory.GetFiles(server, "*.zcfg", IO.SearchOption.TopDirectoryOnly)
                for config in zcfg:
                    zcfg_cleared = re.sub(r"\\[^\\]+$","", config)
                    if update.Contains(zcfg_cleared):
                        process = self.execSQL_process.Start(self.execSQL_path, 'zcfg="' + config + '" sql="' + update + '"')
                        process.WaitForExit() 
                        log.WriteLine("Application de la MaJ BDD : " + update +\
                                      " en utilisant le fichier de configuration :" +\
                                      config)                    

    #Suppression d'une sauvegarde
    def delete(self, index):
        try:
            self.backups[index].delete()
            self.backups.pop(index)
        except(IndexError):
            pass

    def open(self):
        dir = IO.Directory.GetCurrentDirectory()
        dir += BASE_SAVE_DIR.replace(".","")
        Diagnostics.Process.Start("explorer.exe", "/root,"+dir)

#Classe de gestion de la Base de Données
class Database:
    def __init__(self, conf):

        #sauvegarde de la configuration pour usage ultérieur par les sauvegardes
        self.config = conf

        #Récupération des information de configuraiton de la Base de données
        server = self.config.data["SQL"]["server"]
        username = self.config.data["SQL"]["username"]
        password = self.config.data["SQL"]["password"]
        #Création des objets nécessaires à la connexion
        self.string = "Provider=SQLOLEDB;Data Source=" + server + \
                      ";Persist Security Info=True;Password=" + password + ";User ID="+ username
        self.connection = Data.OleDb.OleDbConnection(self.string)
        self.command = Data.OleDb.OleDbCommand()
        self.adapter = Data.OleDb.OleDbDataAdapter()

        #Création d'une liste vide qui contiendra la liste des bases de données
        self.list = []

        

    #Exécution d'UNE requete SQL
    def execute(self,sql):
        #On tente de fermer la connexion si nue connexion s'est mal teminée
        try:
            self.connection.Close()
        except:
            pass
        self.command.Connection = self.connection
        self.command.CommandText = sql
        self.connection.Open()
        self.command.ExecuteNonQuery()
        self.connection.Close()

    def backup_all(self, dest):
        #On sauvegarde chaque base de données
        for db in self.list:
            self.execute(self.sql_backup(db, dest + "\\" + db + ".bak"))
    
    def drop_all(self):
        #On Supprime toutes les bases de données
        try:
            for db in self.list:
                for request in self.sql_delete_database(db):
                    self.execute(request)
        except:
            pass

    def create_all(self):
        #On Crée toutes les bases de données
        for db in self.list:
            self.execute(self.sql_create_database(db))
        pass

    def restore_all(self, sourcedir):
        #On restaure toutes les bases de données depuis les .bak de <sourcedir>
        #self.drop_all() #Tenter la restauration sans Dropper les tables
        for db in self.list:
            for file in IO.Directory.GetFiles(sourcedir,"*.bak",IO.SearchOption.AllDirectories):
                cleanfile = re.sub("^.+\\\\","",file)
                cleanfile = cleanfile.Replace(".bak", "")
                if cleanfile.Contains(db):
                    self.execute(self.sql_restore(db, file))

    #Génère la requète SQL pour sauvegarder une base
    def sql_backup(self, base, file):
        return "BACKUP DATABASE [" + base + "] TO  DISK = '" + file + \
               "' WITH NOFORMAT, NOINIT,  NAME = '" + base + \
               "-Sauvegarde Base de données complète', SKIP, NOREWIND, NOUNLOAD,  STATS = 10"

    #Génère la requète SQL pour restaurer une base
    def sql_restore(self, base, file):
        return "RESTORE DATABASE [" + base + "] FROM  DISK = '" + file + \
               "' WITH  FILE = 1,  NOUNLOAD,  STATS = 10, REPLACE"

    #Génère les deux requetes nécessaire pour supprimer une base
    #La première requète déconnecte tous les utilisateurs de la base de donnée
    #La seconde requète la supprime
    def sql_delete_database(self, base):
        return ["ALTER DATABASE [" + base + "] SET  SINGLE_USER WITH ROLLBACK IMMEDIATE",
                "DROP DATABASE [" + base + "]"]

    #Génère la requète SQL de création d'une base de données
    def sql_create_database(self, base):
        return "CREATE DATABASE " + base