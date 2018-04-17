import pywps

class invest(pywps.Process):
    def __init__(self):
        inputs = [pywps.LiteralInput('name', 'Input name', data_type='string')]
        outputs = [pywps.LiteralOutput('response','Output response', data_type='string')]

        super(invest, self).__init__(
            self._handler,
            identifier='JTS:boundary',
            title='Boundary',
            abstract='Returns a geometry boundary. For polygons, returns a linear ring or multi-linestring equal to the boundary of the polygon(s). For linestrings, returns a multipoint equal to the endpoints of the linestring. For points, returns an empty geometry collection.',
            version='None',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        response.outputs['response'].data = "JTS:boundary process"
        response.outputs['response'].uom = pywps.UOM('unity')
        return response