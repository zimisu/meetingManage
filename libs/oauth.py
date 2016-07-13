from app import cred


auth_endpoint_url = 'https://login.chinacloudapi.cn/%s/oauth2/authorize?%%s' % cred['tenant']
token_endpoint_url = 'https://login.chinacloudapi.cn/%s/oauth2/token' % cred['tenant']
