import natcap.invest.cli
import importlib
import sys

for key, value in natcap.invest.cli._MODEL_UIS.iteritems():
    #get class name
    gui = getattr(value, "gui")
    #create class instance
    if gui != None:
        m, c = gui.split(".")
        m = importlib.import_module(".".join(["natcap.invest.ui", m]))
        c = getattr(m, c)
        i = c()
        for p in i.inputs:
            print p.label
            print p.helptext
            print p.args_key
