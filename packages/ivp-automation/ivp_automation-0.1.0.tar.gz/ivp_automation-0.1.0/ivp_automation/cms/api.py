class Api:
    def __init__(self, url, session_trust_env: bool = False, debug_mode: bool = False):
        self.session = requests.Session()
        self.session.trust_env = session_trust_env
        self.secure_headers = {'X-Requested-With': 'XMLHttpRequest'}
        self.debug_mode = debug_mode
        self.url = url

    def login(self, username: str, password: str):
        url = "%s/cms-etisalat/login?redirect=account/dashboards" % self.url
        response = self.session.get(url=url, allow_redirects=True)
        response.raise_for_status()

        response_soup = BeautifulSoup(response.content, 'html.parser')

        login_token = response_soup.find("input", type="hidden", attrs={"name": "login_token"})["value"]
        payload = {'login_string' : username, 'login_pass' : password, "login_token": login_token}

        login_response = self.session.post(url=url, data=payload, verify=False, allow_redirects=True)
        login_response.raise_for_status()