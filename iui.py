import natcap.invest
import natcap.invest.cli
import importlib
import sys

import pywps
#import pywps.Process
#import pywps.LiteralInput
#import pywps.LiteralOutput
#import pywps.UOM


def handler(self, request, response):
    response.outputs['response'].data = self.identifier
    response.outputs['response'].uom = pywps.UOM('unity')

    return response

def process_generator():
    processes = []
    print "Iterating over InVEST UIs"
    for key, value in natcap.invest.cli._MODEL_UIS.iteritems():
        identifier = key
        print "\n%s" % identifier

        #get class name
        print "Extracting path to GUI definition"
        gui = getattr(value, "gui")
        #create class instance
        if gui != None:
            m, c = gui.split(".")
            print "Importing module"
            m = importlib.import_module(".".join(["natcap.invest.ui", m]))
            print "Getting model class"
            c = getattr(m, c)
            print "Instantiating model"
            i = c()

            title = i.label
            abstract = ""
            print "%s" % title

            version = natcap.invest.__version__

            inputs = []
            outputs = [pywps.LiteralOutput('response',
                                           'Output response',
                                            data_type='string')]

            print "Parsing inputs"
            for p in i.inputs:
                inputs.append(pywps.LiteralInput(p.args_key,
                                                 p.label,
                                                 data_type="string"))
                #print "\t%s" % p.label
                #print p.helptext
                print "\t%s" % p.args_key

            print "Generating PyWPS process"
            processes.append(pywps.Process(handler,
                                           identifier,
                                           title,
                                           abstract,
                                           version,
                                           inputs,
                                           outputs,
                                           True,
                                           True))

            return processes

##        subclass = type(identifier,
##                        (pywps.Process(handler,
##                                       identifier,
##                                       title,
##                                       abstract,
##                                       version,
##                                       inputs,
##                                       outputs,
##                                       True,
##                                       True),),
##                        {})
##                                      
