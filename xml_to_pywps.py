import os
import owslib.wps
from xml.etree import ElementTree


describe_process_path = os.path.join(os.path.dirname(__file__), "xml/JTS:area.xml")
xml = open(describe_process_path).read()

#wps = owslib.wps.WebProcessingService("http://127.0.0.1:8080/geoserver/ows", verbose=False, skip_caps=True)
wps = owslib.wps.WebProcessingService("", verbose=False, skip_caps=True)

process = wps.describeprocess('JTS:area', xml=xml)

for parameter in process.dataInputs:
    owslib.wps.printInputOutput(parameter)

xmlstr = ElementTree.tostring(process._root, encoding='utf8', method='xml')

