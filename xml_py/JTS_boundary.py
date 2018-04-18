import pywps

class invest(pywps.Process):
    def __init__(self):
        inputs = [pywps.ComplexInput('geom', 'Input geometry', supported_formats=[pywps.Format('text/xml; subtype=gml/3.1.1'), pywps.Format('text/xml; subtype=gml/2.1.2'), pywps.Format('application/wkt'), pywps.Format('application/json'), pywps.Format('application/gml-3.1.1'), pywps.Format('application/gml-2.1.2')])]

        outputs = [pywps.ComplexInput('result', 'None', supported_formats=[pywps.Format('text/xml; subtype=gml/3.1.1'), pywps.Format('text/xml; subtype=gml/2.1.2'), pywps.Format('application/wkt'), pywps.Format('application/json'), pywps.Format('application/gml-3.1.1'), pywps.Format('application/gml-2.1.2')])]

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
        return response