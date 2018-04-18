import os
import string

import owslib.wps
import xml.etree.ElementTree

def get_describe_xml(server, process_name):
    wps = owslib.wps.WebProcessingService(server, verbose=False, skip_caps=True)
    process = wps.describeprocess(process_name)

    return xml.etree.ElementTree.tostring(process._root, encoding='utf8', method='xml')

def pywps_header():
    block = """import pywps"""

    return block

def pywps_class(process):
    block = ""
    
    block = block + """\n\nclass invest(pywps.Process):
    def __init__(self):"""

    block = block + """\n        inputs = [%s]"""

    inputs = []
    literal_input_template = "pywps.LiteralInput('%s', '%s', data_type='%s')"
    complex_input_template = "pywps.ComplexInput('%s', '%s', supported_formats=[%s])"
    format_template = "pywps.Format('%s')"
    for parameter in process.dataInputs:
        if parameter.dataType == "LiteralInput":
            inputs.append(literal_input_template % (parameter.identifier,
                                                    parameter.abstract,
                                                    parameter.dataType))
        elif parameter.dataType == "ComplexData":
            formats = []
            for value in parameter.supportedValues:
                formats.append(format_template % value.mimeType)

            inputs.append(complex_input_template % (parameter.identifier,
                                                    parameter.abstract,
                                                    ", ".join(formats)))             
        else:
            raise ValueError, "parameter type %s" % parameter.dataType

    block = block % ", ".join(inputs)

    block = block + """\n\n        outputs = [%s]"""

    outputs = []
    literal_output_template = "pywps.LiteralOutput('%s', '%s', data_type='%s')"
    complex_output_template = "pywps.ComplexInput('%s', '%s', supported_formats=[%s])"
    format_template = "pywps.Format('%s')"

    for parameter in process.processOutputs:
        
        if parameter.dataType == "LiteralData":
            print parameter.identifier
            outputs.append(literal_output_template % (parameter.identifier,
                                                      parameter.abstract,
                                                      parameter.dataType))
        elif parameter.dataType == "ComplexData":
            formats = []
            for value in parameter.supportedValues:
                formats.append(format_template % value.mimeType)

            outputs.append(complex_output_template % (parameter.identifier,
                                                      parameter.abstract,
                                                      ", ".join(formats)))             

        else:
            raise ValueError, "parameter type %s" % parameter.dataType


    block = block % ", ".join(outputs)

    block = block + """\n\n        super(invest, self).__init__(
            self._handler,
            identifier='%s',
            title='%s',
            abstract='%s',
            version='%s',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )"""

    block = block % (process.identifier,
                     process.title,
                     process.abstract,
                     process.processVersion)

    return block
    
def pywps_handler(message):
    block = """\n\n    def _handler(self, request, response):
        return response"""

    return block

def xml_to_pywps(xml, py):
    wps = owslib.wps.WebProcessingService("", verbose=False, skip_caps=True)
    process = wps.describeprocess("", xml=xml)

    #print dir(process)
    
    py.write(pywps_header())
    py.write(pywps_class(process))    
    py.write(pywps_handler(process.identifier))

    return process

if __name__ == "__main__":
##    xml = get_describe_xml("http://127.0.0.1:8080/geoserver/ows", "JTS:area")

    print "Generating PyWPS scripts from WPS XML"
    xml_path = os.path.join(os.path.dirname(__file__), "xml_py")
    for describe_process_path in os.listdir(xml_path):
        if describe_process_path.endswith(".xml"):
            print "Processing %s" % describe_process_path
            stem, _ = os.path.splitext(describe_process_path)

            translator = string.maketrans(string.punctuation, "_" * len(string.punctuation))
            stem = stem.translate(translator) + ".py"

            describe_process_path = os.path.join(xml_path,
                                                 describe_process_path)
            
            python_process_path = os.path.join(xml_path,
                                               stem)  

            process = xml_to_pywps(open(describe_process_path).read(),
                                   open(python_process_path, 'w'))

            break
