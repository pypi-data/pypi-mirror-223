# datalaboauthenticator
Custom Oauthenticator to manage the Oauth2 process in the [datalab project](https://github.com/ifca-datalab/). This authenticator gives users coming from the portal an automatic user account to access their jupyter session without having to login again in the OpenID provider. 

This authenticafor inherits from the Generic Authenticator and it has been tested through our internal Keycloak instance.

## Installation

### Manual

Download and install the repository inside the image used to deploy the jupyterhub session.
```
git clone https://github.com/aidaph/datalaboauthenticator
pip install .
```
## Configuration in jupyterhub config
Define the following lines in the jupyterhub_config.py file:

```python
c.JupyterHub.authenticator_class = "datalab-oauth"
c.DatalabOAuthenticator.client_id = 'datalab-client' # oauth2 client id for your app
c.DatalabOAuthenticator.client_secret = 'datalab-secret' # oauth2 client secret for your app
c.DatalabOAuthenticator.login_service = "SSO"
c.DatalabOAuthenticator.authorize_url = "https://sso.ifca.es/auth/realms/datalab/protocol/openid-connect/auth"
c.DatalabOAuthenticator.token_url = 'https://sso.ifca.es/auth/realms/datalab/protocol/openid-connect/token' # oauth2 provider's token url
c.DatalabOAuthenticator.userdata_url = 'https://sso.ifca.es/auth/realms/datalab/protocol/openid-connect/userinfo' # oauth2 provider's endpoint with user data
c.DatalabOAuthenticator.oauth_callback_url = 'https://{}.datalab.ifca.es/hub/oauth_callback'.format(os.environ['NAMESPACE'])
c.DatalabOAuthenticator.scope = ["profile","openid", "email", "groups"]
c.DatalabOAuthenticator.userdata_params = {"state": "state"} # params to send for userdata endpoint
c.DatalabOAuthenticator.username_claim = "email"
c.DatalabOAuthenticator.allowed_groups = ["dummy"]
c.DatalabOAuthenticator.username_key = "preferred_username" # username key from json returned from user data endpoint
c.DatalabOAuthenticator.extra_authorize_params = {"token": '{}'.format(os.environ["ACCESS_TOKEN"])}
```

Take into account that the authenticator makes the auto_login as soon as the user comes from the portal without showing the Log in button. This behavior can be swittched off turning the `DatalabOAuthenticator.auto_login" option to `False`. 
