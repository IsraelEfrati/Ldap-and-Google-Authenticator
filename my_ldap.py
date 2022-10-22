from ldap3 import Server, Connection, ALL, SUBTREE, SAFE_SYNC
from ldap3.core.exceptions import LDAPException, LDAPBindError
from pyotp import random_base32, totp


def get_secret():
    with open("code.txt") as f:
        line = f.readline()
    if line:
        secret = line
    else:
        secret = random_base32()
    return secret


SECRET = get_secret()
OTP = totp.TOTP(SECRET)


def connect_ldap_server(full_name, password):
    try:
        # Provide the hostname and port number of the openLDAP
        server_uri = f"ldap://192.168.25.130:389"
        server = Server(server_uri, get_info=ALL)
        # username and password can be configured during openldap setup
        user = "cn={},cn=my_users,dc=example,dc=org".format(full_name)
        connection = Connection(server,
                                user=user,
                                password=password)
        bind_response = connection.bind()  # Returns True or False
        return bind_response
    except LDAPBindError as e:
        connection = e


def create_qr_code(user):
    global OTP
    path_start = "https://www.google.com/chart?chs=200x200&chld=M%7C0&cht=qr&chl="
    partial_path = OTP.provisioning_uri(name=user, issuer_name='israel_ldap')
    full_path = path_start + (partial_path)
    return full_path


def check_google_code(google_code):
    verified = OTP.verify(google_code)
    return verified
