class AuthenticatedRequests:

    def __init__(self, requests):
        self.requests = requests
        self.session = requests.Session()
        
    def basic_auth_request(self,
        username, 
        password,
        url,
        method = 'GET',
        params=None,
        data=None,
        headers=None,
        cookies=None):
        
        self.session.auth = (username, password)
        return self.session.request(method=method, url=url, params=params, data=data, headers=headers, cookies=cookies)
    
    def api_key_auth_request(self,
        api_key_key,
        api_key_value,
        api_key_add_to,
        url,
        method = 'GET',
        params=None,
        data=None,
        headers=None,
        cookies=None):

        if api_key_add_to == 'Header':
            if (headers is None):
                headers = {}
            headers[api_key_key] = api_key_value
        elif api_key_add_to == 'QueryParams':
            if (url.find('?') == -1):
                url = url + '?' + api_key_key + '=' + api_key_value
            else:
                url = url.replace("?", '?' + api_key_key + '=' + api_key_value + '&')
        else:
            raise ValueError('Unknown api_key_add_to: ' + api_key_add_to)

        return self.session.request(method=method, url=url, params=params, data=data, headers=headers, cookies=cookies)

    def oauth_password_flow(self,
        token_url,
        client_id,
        client_secret,
        username,
        password,
        url,
        method = 'GET',
        params=None,
        data=None,
        headers=None,
        cookies=None):
        
        ## Request parameters
        data = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password,
        }
        # Send a POST request to the token endpoint
        response = self.requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            if (headers is None):
                headers = {}
            headers['Authorization'] = token_data['access_token']

            return self.session.request(method=method, url=url, params=params, data=data, headers=headers, cookies=cookies)
        else:
            raise ValueError(f'Failed to get access token. Status code {response.status_code}')

        
