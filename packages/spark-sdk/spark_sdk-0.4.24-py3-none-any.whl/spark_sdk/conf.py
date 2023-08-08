HADOOP_HOST = "hdfs://hdfs-cluster.datalake.bigdata.local"
HADOOP_PORT = 8020
HIVE_IP_NODES1 = "master01-dc9c14u40.bigdata.local:9083"
HIVE_IP_NODES2 = "master02-dc9c14u41.bigdata.local:9083"

GMS_AUTH_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImR1eXZuYyIsInR5cGUiOiJQRVJTT05BTCIsInZlcnNpb24iOiIyIiwianRpIjoiMmMxMDM2MzQtNjI5My00OTM3LWFlYzctNTI0YmEyMzI3MGZlIiwic3ViIjoiZHV5dm5jIiwiaXNzIjoiZGF0YWh1Yi1tZXRhZGF0YS1zZXJ2aWNlIn0.zJISXPTw1HCI2lDIC0pfSACCg2GLfnRNVPfWBif8b88"
# GMS_URL_KEY = "http://ccatalog-gms.cads.live"
GMS_URL_KEY = "http://ccatalog-gms.cads.live"

import os
from urllib.parse import urlparse
domain = urlparse(GMS_URL_KEY).netloc
no_proxy = os.getenv('no_proxy')

if no_proxy:
    if 'ccatalog-gms.cads.live,git.cads.live,vault.cads.live' in no_proxy:
        pass
    else:
        os.environ['no_proxy'] = os.getenv('no_proxy')+","+domain+","+"git.cads.live,vault.cads.live"
else:
    os.environ['no_proxy'] = domain+","+"git.cads.live,vault.cads.live"