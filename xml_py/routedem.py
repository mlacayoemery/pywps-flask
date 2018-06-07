import pywps
import pywps.validator.mode

import natcap.invest.routing.routedem
import tempfile
import os.path

import logging
import sys

class invest(pywps.Process):
    def __init__(self):
        inputs = [pywps.LiteralInput("calculate_downstream_distance",
                                     "Calculate Downstream Distance",
                                     data_type="boolean"),
                  pywps.LiteralInput("calculate_flow_accumulation",
                                     "Calculate Flow Accumulation",
                                     data_type="boolean"),
                  pywps.LiteralInput("calculate_slope",
                                     "Calculate Slope",
                                     data_type="boolean"),
                  pywps.LiteralInput("calculate_stream_threshold",
                                     "Calculate Stream Threshold",
                                     data_type="boolean"),
                  pywps.LiteralInput("threshold_flow_accumulation",
                                     "Threshold Flow Accumulation",
                                     data_type="integer"),
                  pywps.ComplexInput('dem',
                                     'DEM',
                                     supported_formats=[pywps.Format('image/tiff')],
                                     mode=pywps.validator.mode.MODE.STRICT)]

        outputs = [pywps.ComplexOutput('route',
                                       'Route',
                                       supported_formats=[pywps.Format('image/tiff')])]

        super(invest, self).__init__(
            self._handler,
            identifier='routedem', #'natcap.invest.routing.routedem',
            title='RouteDEM',
            abstract='InVEST implementation of Tarboton (1997) d-infinity flow direction algorithm.',
            version='None',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        logger = logging.getLogger("natcap.invest.routing.routedem")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        
        args = {
            u'calculate_downstream_distance': request.inputs["calculate_downstream_distance"][0].data,
            u'calculate_flow_accumulation': request.inputs["calculate_flow_accumulation"][0].data,
            u'calculate_slope': request.inputs["calculate_slope"][0].data,
            u'calculate_stream_threshold': request.inputs["calculate_stream_threshold"][0].data,
            u'dem_path': request.inputs['dem'][0].file,
            u'results_suffix': u'',
            u'threshold_flow_accumulation': request.inputs["threshold_flow_accumulation"][0].data,
            u'workspace_dir': tempfile.mkdtemp(),
        }

        natcap.invest.routing.routedem.execute(args)

        response.outputs['route'].file = os.path.join(args[u'workspace_dir'],
                                                      "flow_direction.tif")

        return response
