import os
import json

import pprint

source_path = os.path.join(os.path.dirname(__file__), "iui")
destination_path = os.path.join(os.path.dirname(__file__), "xml")

data_types = {"folder" : "LiteralData",
              "text" : "LiteralData",
              "file" : "ComplexData",
              "checkbox" : "LiteralData",
              "dropdown" : "LiteralData",
              "float" : "LiteralData",
              "multi" : "ComplexData",
              "OGRFieldDropdown" : "ComplexData"}

ignore = ["natcap.invest.coastal_vulnerability.coastal_vulnerability",
          "natcap.invest.fisheries.fisheries_hst",
          "natcap.invest.scenic_quality.scenic_quality",
          "natcap.invest.wind_energy.wind_energy",
          "natcap.invest.fisheries.fisheries",
          "natcap.invest.finfish_aquaculture.finfish_aquaculture",
          "natcap.invest.habitat_risk_assessment.hra_preprocessor",
          "natcap.invest.pollination.pollination",
          "natcap.invest.coastal_blue_carbon.preprocessor",
          "natcap.invest.scenario_generator.scenario_generator",
          "natcap.invest.recreation.recmodel_client",
          "natcap.invest.coastal_blue_carbon.coastal_blue_carbon",
          "natcap.invest.seasonal_water_yield.seasonal_water_yield",
          "natcap.invest.globio",
          "natcap.invest.carbon",
          "natcap.invest.wave_energy.wave_energy",
          "natcap.invest.hydropower.hydropower_water_yield"]

def parse_element(element):
    if "type" in element.keys():
        type_key = "type"
    elif "dataType" in elements.keys():
        type_key = "dataType"
    else:
        raise KeyError, "Element missing type"

    if element[type_key] == "label":
        return None

    e = {}
    e["identifier"] = element["id"]
    e["title"] = element["label"]

    try:
        e["abstract"] = element["helpText"]
    except KeyError:
        e["abstract"] = ""

    e["type"] = data_types[element[type_key]]

    if e["type"] == "multi" or e["type"] == "checkbox" or element.get("required") == True:
        e["minOccurs"] = 1
    else:
        e["minOccurs"] = 0

    e["maxOccurs"] = 1

    return e
    
if __name__ == "__main__":
    models = []
    for file_name in os.listdir(source_path):
        if file_name.endswith(".json"):
            #print "\t\t\t\t%s" % file_name
            model = json.load(open(os.path.join(source_path, file_name)))

            identifier = model["targetScript"] #model["modelName"]

            if not model["targetScript"] in ignore:           
            
                title = model["label"]
                abstract = ""

                element_list = model["elements"]

                options = []
                print "\n%s" % identifier
                    
                for e in element_list:
                    options.append(e["id"].replace("_container",""))

                if options[0] == "workspace_list":
                    options[0] = "base"
                elif options[0] == "routedem_list":
                    options[0] = "base"
                else:
                    raise ValueError, "workspace_list missing"

                print "options: %s" % ", ".join(options)

                for elements in element_list:
                    #print "variant: %s" % elements["id"]
                    
                    if "collapsible" in elements.keys():
                        elements = elements["elements"][0]

                    if "elements" in elements.keys():
                        elements = elements["elements"]
                    else:
                        elements = [elements]
                    
                    inputs = []
                    for e in elements:
                        i = parse_element(e)

                        if i != None:
                            #print "\t%s" % i["identifier"]
                            inputs.append(i)

                    models.append([identifier,
                                   title,
                                   abstract,
                                   inputs])
            
        #break
            
            
