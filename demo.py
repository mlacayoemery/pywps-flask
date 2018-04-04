#!/usr/bin/env python3

# Copyright (c) 2016 PyWPS Project Steering Committee
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import dill

import os
import flask

import pywps
from pywps import Service

from processes.sleep import Sleep
from processes.ultimate_question import UltimateQuestion
from processes.centroids import Centroids
from processes.sayhello import SayHello
from processes.feature_count import FeatureCount
from processes.buffer import Buffer
from processes.area import Area
from processes.bboxinout import Box
from processes.jsonprocess import TestJson

from processes.echo import Echo

import uiparse

#http://127.0.0.1:5000/wps?REQUEST=GetCapabilities&SERVICE=WPS&VERSION=1.0.0

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="InVEST WPS Server")
    parser.add_argument("-n", "--newpickle",
                        help="Creates a new pickle of the InVEST processes",
                        action="store_true")    
    parser.add_argument('-d',
                        '--daemon',
                        action='store_true',
                        help="run in daemon mode")
    parser.add_argument('-a',
                        '--all-addresses',
                        action='store_true',
                        help="run flask using IPv4 0.0.0.0 (all network interfaces),"  +  
                            "otherwise bind to 127.0.0.1 (localhost).  This maybe necessary in systems that only run Flask")
    args = parser.parse_args()

    ppath = os.path.join(os.path.dirname(__file__),"invest.p")
    
    app = flask.Flask(__name__)

    processes = [
        FeatureCount(),
        SayHello(),
        Centroids(),
        UltimateQuestion(),
        Sleep(),
        Buffer(),
        Area(),
        Box(),
        TestJson(),
        Echo()
    ]

    if args.newpickle or not os.path.exists(ppath):
        print "Parsing InVEST metadata from package"
        invest = uiparse.process_generator()
        print "Pickling InVEST"
        dill.dump(invest, open(ppath, 'w'))

    print "Loading InVEST pickle"
    invest = dill.load(open(ppath))
    print "Extending default process list with InVEST"    
    processes.extend(invest)
    print "Finished processing InVEST"

    # For the process list on the home page
    print "Generating metadata for home page"
    process_descriptor = {}
    for process in processes:
        abstract = process.abstract
        identifier = process.identifier
        process_descriptor[identifier] = abstract

    print "Starting PyWPS instance"
    #print processes
    # This is, how you start PyWPS instance
    service = Service(processes, ['pywps.cfg'])
    print "PyWPS instance running"


    @app.route("/")
    def hello():
        server_url = pywps.configuration.get_config_value("server", "url")
        request_url = flask.request.url
        return flask.render_template('home.html', request_url=request_url,
                                     server_url=server_url,
                                     process_descriptor=process_descriptor)


    @app.route('/wps', methods=['GET', 'POST'])
    def wps():

        return service


    @app.route('/outputs/'+'<filename>')
    def outputfile(filename):
        targetfile = os.path.join('outputs', filename)
        if os.path.isfile(targetfile):
            file_ext = os.path.splitext(targetfile)[1]
            with open(targetfile, mode='rb') as f:
                file_bytes = f.read()
            mime_type = None
            if 'xml' in file_ext:
                mime_type = 'text/xml'
            return flask.Response(file_bytes, content_type=mime_type)
        else:
            flask.abort(404)


    @app.route('/static/'+'<filename>')
    def staticfile(filename):
        targetfile = os.path.join('static', filename)
        if os.path.isfile(targetfile):
            with open(targetfile, mode='rb') as f:
                file_bytes = f.read()
            mime_type = None
            return flask.Response(file_bytes, content_type=mime_type)
        else:
            flask.abort(404)

    if args.all_addresses:
        bind_host='0.0.0.0'
    else:
        bind_host='127.0.0.1'

    if args.daemon:
        pid = None
        try:
            pid = os.fork()
        except OSError as e:
            raise Exception("%s [%d]" % (e.strerror, e.errno))

        if (pid == 0):
            os.setsid()
            app.run(threaded=True,host=bind_host)
        else:
            os._exit(0)
    else:
        app.run(threaded=True,host=bind_host)
