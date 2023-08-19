from app.utils.constants import Key, Template, Environment, Url

def render_error_page(self, status_code=504, title="Technical Error", message="Something went wrong\nPlease try again", redirect_url = None, redirect_text = None):
    error =  {"error":{
        Key.STATUS_CODE: status_code,
        Key.TITLE: title,
        Key.MESSAGE: message,
        Key.REDIRECT_URL: redirect_url,
        Key.REDIRECT_TEXT: redirect_text
    }}

    self.render(Template.ERROR, **error)


def get_mapped_records(cursor, want_one_if_one=True):
    if cursor.rowcount > 0:
        all_data = cursor.fetchall()

        records = []
        columns = [column[0] for column in cursor.description]

        for data in all_data:
            record = dict(zip(columns, data))
            records.append(record)

        if len(records)==1 and want_one_if_one:
            return records[0]
        else:
            return records
    else:
        None


def redirect_to_cas_login_page(self):
    # original_proto = self.request.headers.get("X-Forwarded-Proto", "")
    # original_host = self.request.headers.get("X-Forwarded-Host", "")
    # # Construct the full URL with the original scheme and hostname
    # full_url = f"{original_proto}://{original_host}{self.request.uri}"
    # print(f"full_url:{full_url}")

    print("Redirecting to cas login page")
    cas_login_url = get_cas_login_page_url(self)
    self.redirect(cas_login_url)


def get_cas_login_page_url(self):
    environment = self.application.environment
    if environment == Environment.PROD: environment = ""

    host_url = self.request.full_url()
    print(f"host_url:{host_url}")

    cas_login_url = Url.CAS_LOGIN_URL.replace("ENVIRONMENT",environment).replace("HOST_URL",host_url).rstrip("/")
    print(f"cas_login_url:{cas_login_url}")

    return cas_login_url


def set_cookie(self, key, payload):
    print(f'Setting cookie for key:{key} ...')
    self.set_secure_cookie(
        key, 
        str(payload if (key==Key.TOKEN) else payload[key])
    )

def get_cookie(self, key):
    print(f'Getting cookie for key:{key} ...')
    data = self.get_secure_cookie(key)
    return data