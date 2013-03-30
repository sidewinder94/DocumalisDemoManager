#!/bin/python
# -*- coding: utf-8 -*-
import wpf
import clr

clr.AddReference("System.Windows.Forms")

from System.Windows import Application, Forms
from model import *
from controller import *
from view import *

#Lancement du programme
if __name__ == '__main__':
    try:
        model = Model()
        view = View(model)
        controller = Controller(view, model)

        (Application().Run(view))
    except Exception, e:
        log = None
        if IO.File.Exists(".MainErrorLog.log"):
            log = IO.File.AppendText(".MainErrorLog.log")
        else:
            log = IO.File.CreateText(".MainErrorLog.log")
        log.WriteLine(str(time.strftime("%d-%m-%Y %H-%M-%S",time.localtime())))
        log.WriteLine(e)
        log.WriteLine("\n")
        try:
            log.Close()
        except:
            pass
        Forms.MessageBox.Show("L'application vient de planter !\n" + \
                              "Merci de consulter le log pour en connaitre la raison",
                              "I Just Crashed !",Forms.MessageBoxButtons.OK,
                              Forms.MessageBoxIcon.Error)