import pywps

class invest(pywps.Process):
    def __init__(self):
        inputs = [pywps.LiteralInput('name', 'Input name', data_type='string')]
        outputs = [pywps.LiteralOutput('response','Output response', data_type='string')]

        super(invest, self).__init__(
            self._handler,
            identifier='JTS:area',
            title='Area',
            abstract='Returns the area of a geometry, in the units of the geometry. Assumes a Cartesian plane, so this process is only recommended for non-geographic CRSes.',
            version='None',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        response.outputs['response'].data = "JTS:area process"
        response.outputs['response'].uom = pywps.UOM('unity')
        return response