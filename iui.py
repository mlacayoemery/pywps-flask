import natcap.invest.cli
import importlib
import sys

def module_list(pkg):
    import pkgutil
    import os.path

    pkgpath = os.path.dirname(pkg.__file__)
    return [name for _, name, _ in pkgutil.iter_modules([pkgpath])]

#print module_list(natcap.invest)

##models = ['carbon',
##          'coastal_blue_carbon',
##          'coastal_vulnerability',
##          'crop_production_percentile',
##          'crop_production_regression',
##          'finfish_aquaculture',
##          'fisheries',
##          'forest_carbon_edge_effect',
##          'globio',
##          'habitat_quality',
##          'habitat_risk_assessment',
##          'habitat_suitability',
##          'hydropower',
##          'ndr',
##          'overlap_analysis',
##          'pollination',
##          'recreation',
##          'routing',
##          'scenario_gen_proximity',
##          'scenario_generator',
##          'scenic_quality',
##          'sdr',
##          'seasonal_water_yield',
##          'wave_energy',
##          'wind_energy']
##
##for name in models:
##    print name

##models = natcap.invest.cli._MODEL_UIS.keys()
##models.sort()


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
