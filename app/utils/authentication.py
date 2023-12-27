import jwt
import bcrypt

from .constants import Key, Token
from .common import redirect_to_cas_login_page, render_error_page, get_cas_login_page_url, get_cookie
from app import settings


class JwtToken():
    def validate(self, token=None):
        print("\nValidating token ...")

        decoded_payload = None
        token_received_from_cas = True

        if token is None:
            token = get_cookie(self, Key.TOKEN)
            token_received_from_cas = False


        if token:
            token_detail = self.application.token_detail
            if token_detail:

                decoded_payload = None
                try:
                    print(f"token: {token}")
                    decoded_payload = jwt.decode(token, token_detail[Token.PRIVATE_KEY], algorithms=[token_detail[Token.ALGORITHM]])

                    print(f"decoded_payload: {decoded_payload}")
                    if decoded_payload is None:
                        print("Payload is None")
                        if token_received_from_cas:
                            render_error_page(self, message="Please try logging in again.", redirect_url=get_cas_login_page_url(self), redirect_text="Try Login Again")
                        else:
                            render_error_page(
                                self, message="Some issue has been encountered on perfoming this. Please try loggin in",
                                redirect_url=get_cas_login_page_url(self), redirect_text="Login"
                            )

                except jwt.ExpiredSignatureError:
                    print("Token has expired")

                    if token_received_from_cas:
                        render_error_page(self, message="Please try logging in again.", redirect_url=get_cas_login_page_url(self), redirect_text="Login Again")
                    else:
                        render_error_page(
                            self, status_code=401, title="Session Expired", message="Your session has been expired. Please login to continue",
                            redirect_url=get_cas_login_page_url(self), redirect_text="Login"
                        )
                        
                except jwt.InvalidTokenError:
                    print("Invalid token")
                    if token_received_from_cas:
                        render_error_page(self, message="Please try logging in again.", redirect_url=get_cas_login_page_url(self), redirect_text="Login Again")
                    else:
                        redirect_to_cas_login_page(self)

            else:
                print("Received null token detail from application")
                render_error_page(
                    self, message="Some issue has been encountered on perfoming this task. Please try logging in",
                    redirect_url=get_cas_login_page_url(self), redirect_text="Login"
                )
        else:
            print("Received null token from session")
            redirect_to_cas_login_page(self)
            
        return decoded_payload


class Password():

    def encrypt(password):
        print(f"Encrypting password ...")

        # Generating a salt
        salt = bcrypt.gensalt()
        
        # Hashing the password using the generated salt
        hashed_password = bcrypt.hashpw(password.encode(settings.PASSWORD_ENCODING_STANDARD), salt)
        return {Key.SALT_VALUE:salt, Key.HASHED_PASSWORD:hashed_password}
    

    def is_valid(stored_password_detail, provided_password):
        if stored_password_detail and provided_password:
            stored_salt = stored_password_detail[Key.SALT_VALUE]
            stored_hashed_password = stored_password_detail[Key.HASHED_PASSWORD]

            return stored_hashed_password.encode(settings.PASSWORD_ENCODING_STANDARD) == bcrypt.hashpw(provided_password.encode(settings.PASSWORD_ENCODING_STANDARD), stored_salt.encode(settings.PASSWORD_ENCODING_STANDARD))
        else:
            raise RuntimeError("Stored password detail or provided password is null")