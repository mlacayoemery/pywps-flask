import owslib.wps

wps_url= "http://127.0.0.1:5000/wps"
wps = owslib.wps.WebProcessingService(wps_url, verbose=False, skip_caps=True)

process_name = "routedem"

#dem = owslib.wps.ComplexDataInput('file:///home/mlacayo/workspace/data/Base_Data/Freshwater/dem2.tif')
dem = owslib.wps.ComplexDataInput('http://127.0.0.1:8080/geoserver213/invest/wms?service=WMS&version=1.1.0&request=GetMap&layers=invest:dem2&styles=&bbox=447466.6938,4902500.4053,479896.6938,4952570.4053&width=497&height=768&srs=EPSG:26910&format=image%2Fgeotiff')
dem.get = dem.getXml

inputs = [('calculate_downstream_distance', 'True'),
          ('calculate_flow_accumulation', 'True'),
          ('calculate_slope', 'True'),
          ('calculate_stream_threshold', 'True'),
          ('dem', dem),
          ('threshold_flow_accumulation', '1000')]

execution = wps.execute(process_name, inputs, output = "OUTPUT")
