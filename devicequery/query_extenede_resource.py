#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# This file is part of the jetson_stats package (https://github.com/rbonghi/jetson_stats or http://rnext.it).
# Copyright (c) 2019 Raffaello Bonghi.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from jtop import jtop
import json
import requests


if __name__ == "__main__":

    print("Simple Tegrastats reader")

    with jtop() as jetson:
    # Read tegra stat
        a= str(jetson.stats['GR3D']['frq'])
        print(a)
        hostname = jetson.local_interfaces['hostname']
        print(hostname)
        data = [{'op': 'add', 'path': '/status/capacity/GPU.com~1frq', 'value':a }]
        jsonstring = json.dumps(data)
        print(jsonstring)
        hostip = '192.168.1.93:6443'
        urlstring = 'https://'+hostip+'/api/v1/nodes/'+hostname+'/status'
        try :
            httpresp = requests.patch(url =urlstring , data=jsonstring, headers= {'Content-Type':'application/json-patch+json', 'Authorization' : 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2d3h5VkZUb2FQQUIzT2tJdzRpMVZ3VXlaN1dnNHlhd3lDZmJDMlRmdlEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tZzlnYzgiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjNmYzFjM2Y3LWMyZTYtNGQzMi1hNzM3LWFkNTAyZTQwYzBjZiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.Df2baNwvgvcbm2sH5fcwx0opljO6jO7uFob19ScSNO-G0w0AO3F_mITSiOddsfyFurxoJqrMQnb4d1hKE8QERFpl2cuFFHTn5iCOOtSRoIRhRULAH6CU9xibZH3LLqDVlNqcr9FhzsvDcL9_QnsgROXBhMG3Q5eeRA-zpjoq5gQ_O0w2TGKMxOajwWIyo_1BgGM44dDHL0sL8DKXnOUSIA8baNxhdBph6fcbNSZxVZ68mq6LanK-wFz2B7E0LsHZIP2DPrKaaBb2XA6O8FseeEh6eTuZVBRrIi1-8-NQYLk6rWMFxawSgVlYaQ-KT4PRi4GnXQP5fToBGV7EE7MJfw'},verify=False)
            print(httpresp)
        except Exception as e:
            print(e)

