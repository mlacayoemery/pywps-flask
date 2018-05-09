import pywps

class invest(pywps.Process):
    def __init__(self):
        inputs = [pywps.ComplexInput('geom', 'Input geometry', supported_formats=[pywps.Format('text/xml; subtype=gml/3.1.1'), pywps.Format('text/xml; subtype=gml/2.1.2'), pywps.Format('application/wkt'), pywps.Format('application/json'), pywps.Format('application/gml-3.1.1'), pywps.Format('application/gml-2.1.2')])]

        outputs = [pywps.LiteralOutput('result', 'None', data_type='string')]

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
        return response
