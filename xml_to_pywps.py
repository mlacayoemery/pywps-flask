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

    block = block + """\n        inputs = [pywps.LiteralInput('name', 'Input name', data_type='string')]"""

    block = block + """\n        outputs = [pywps.LiteralOutput('response','Output response', data_type='string')]"""

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
        response.outputs['response'].data = "%s process"
        response.outputs['response'].uom = pywps.UOM('unity')
        return response"""

    block = block % message

    return block

def xml_to_pywps(xml, py):
    wps = owslib.wps.WebProcessingService("", verbose=False, skip_caps=True)
    process = wps.describeprocess("", xml=xml)

    print dir(process)
    
    py.write(pywps_header())
    py.write(pywps_class(process))    
    py.write(pywps_handler(process.identifier))

if __name__ == "__main__":
##    xml = get_describe_xml("http://127.0.0.1:8080/geoserver/ows", "JTS:area")

    for describe_process_path in os.path.join(os.path.dirname(__file__), "xml"):
        if describe_process_path.endswith(".xml"):
            head, tail = os.path.split(describe_process_path)
            translator = string.maketrans(string.punctuation, "_" * len(string.punctuation))
            tail = tail.rstrip(".xml").translate(translator) + ".py"
            python_process_path = os.path.join(head, tail)  

            xml_to_pywps(open(describe_process_path).read(),
                         open(python_process_path, 'w'))
