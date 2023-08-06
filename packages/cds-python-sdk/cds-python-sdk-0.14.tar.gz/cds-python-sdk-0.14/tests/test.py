from capitalonline.common import client, credential
from capitalonline.common.profile import client_profile, http_profile

http_pf = http_profile.HttpProfile()
http_pf.endpoint = 'cdsapi.capitalonline.net/ccs/'
http_pf.reqMethod = 'POST'
http_pf.reqTimeout = 60

client_pf = client_profile.ClientProfile(httpProfile=http_pf)
client_pf.signMethod = 'HMAC-SHA1'
cre = credential.Credential(secret_id='你的ak', secret_key='你的sk')
data = {"InstanceId": "bf02ca19-0180-4d69-90de-e05d1577930a"}
res = client.Client(service='ccs', version='2019-08-08', credential=cre, region='Beijing', profile=client_pf).call(action='DescribeInstances', params=data)
print(res)
