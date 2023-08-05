from oauthenticator.generic import GenericOAuthenticator
from traitlets import default

class DatalabOAuthenticator(GenericOAuthenticator):

    @default("auto_login")
    def _auto_login_default(self):
        """
        The Authenticator base class' config auto_login defaults to False, but
        we change that default to True in TmpAuthenticator. This makes users
        automatically get logged in when they hit the hub's home page, without
        requiring them to click a 'login' button.

        JupyterHub admins can still opt back to present the /hub/login page with
        the login button like this:

            c.TmpAuthenticator.auto_login = False
        """
        return True

    async def authenticate(self, handler, data=None, **kwargs):
        """
        A JupyterHub Authenticator's authenticate method's job is:

        - return None if the user isn't successfully authenticated
        - return a dictionary if authentication is successful with name, admin
          (optional), and auth_state (optional)

        Subclasses should not override this method.

        ref: https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html#authenticator-authenticate-method
        ref: https://github.com/jupyterhub/jupyterhub/blob/4.0.0/jupyterhub/auth.py#L581-L611
        """
        if "token" in self.extra_authorize_params:
            token_info = {
                "access_token": self.extra_authorize_params["token"],
                "token_type":"bearer"
            }
            try: 
                user_info = await self.token_to_user(token_info)
            except:
                # Request new token because this is invalid
                access_token_params = self.build_access_tokens_request_params(handler, data)
                # exchange the oauth code for an access token and get the JSON with info about it
                token_info = await self.get_token_info(handler, access_token_params)
                # use the access_token to get userdata info
                user_info = await self.token_to_user(token_info)
            else:
                self.log.info(f"User INFO in PARAMS: {user_info}")
        # extract the username out of the user_info dict and normalize it
        username = self.user_info_to_username(user_info)
        username = self.normalize_username(username)

        # check if there any refresh_token in the token_info dict
        refresh_token = token_info.get("refresh_token", None)
        if self.enable_auth_state and not refresh_token:
            self.log.debug(
                "Refresh token was empty, will try to pull refresh_token from previous auth_state"
            )
            refresh_token = await self.get_prev_refresh_token(handler, username)
            if refresh_token:
                token_info["refresh_token"] = refresh_token

        # build the auth model to be read if authentication goes right
        auth_model = {
            "name": username,
            "admin": True if username in self.admin_users else None,
            "auth_state": self.build_auth_state_dict(token_info, user_info),
        }

        # update the auth_model with info to later authorize the user in
        # check_allowed, such as admin status and group memberships
        return await self.update_auth_model(auth_model)