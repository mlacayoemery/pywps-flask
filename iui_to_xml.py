import os
import json

import pprint

source_path = os.path.join(os.path.dirname(__file__), "iui")
destination_path = os.path.join(os.path.dirname(__file__), "xml")

data_types = {"folder" : "LiteralData",
              "text" : "LiteralData",
              "file" : "ComplexData",
              "checkbox" : "LiteralData",
              "dropdown" : "LiteralData"}

ignore = ["natcap.invest.coastal_vulnerability.coastal_vulnerability",
          "natcap.invest.fisheries.fisheries_hst",
          "natcap.invest.scenic_quality.scenic_quality",
          "natcap.invest.wind_energy.wind_energy",
          "natcap.invest.fisheries.fisheries",
          "natcap.invest.finfish_aquaculture.finfish_aquaculture",
          "natcap.invest.habitat_risk_assessment.hra_preprocessor"]

models = []
for file_name in os.listdir(source_path):
    if file_name.endswith(".json"):
        model = json.load(open(os.path.join(source_path, file_name)))

        identifier = model["targetScript"] #model["modelName"]

        if not identifier in ignore:           
        
            title = model["label"]
            abstract = ""

            elements = model["elements"]
            print "%s:%s" % (identifier, "-".join(["0"] * len(elements)))
            options = []
            if len(elements) > 1:
                for e in elements:
                    options.append(e["id"])
            print "-".join(options)
            elements=elements[0]["elements"]

            inputs = []
            for e in elements:
                if e["type"] != "label":
                    i = {}
                    i["identifier"] = e["id"] #= e["args_id"]
                    i["title"] = e["label"]

                    try:
                        i["abstract"] = e["helpText"]
                    except KeyError:
                        i["abstract"] = ""

                    i["type"] = data_types[e["type"]]

                    if e["type"] == "checkbox":
                        e["required"] = True

                    if e["required"] == True:
                        i["minOccurs"] = 1
                    else:
                        i["minOccurs"] = 0
                    i["maxOccurs"] = 1

                    print "\t%s" % i["identifier"]
                    inputs.append(i)

            models.append([identifier,
                           title,
                           abstract,
                           inputs])
        
    #break
        
        
