
from pywps import Process, LiteralInput, LiteralOutput, UOM

#http://127.0.0.1:5000/wps?REQUEST=DescribeProcess&IDENTIFIER=echo&SERVICE=WPS&VERSION=1.0.0
#http://127.0.0.1:5000/wps?REQUEST=Execute&IDENTIFIER=echo&DATAINPUTS=message=Hello%20%20World!&SERVICE=WPS&VERSION=1.0.0

class Echo(Process):
    def __init__(self):
        inputs = [LiteralInput('message', 'Input message', data_type='string')]
        outputs = [LiteralOutput('echo',
                                 'Output message', data_type='string')]

        super(Echo, self).__init__(
            self._handler,
            identifier='echo',
            title='Echo Test',
            abstract='Returns the given literal string',
            version='1.0.0.0',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        response.outputs['echo'].data = request.inputs['message'][0].data
        response.outputs['echo'].uom = UOM('unity')
        return response
