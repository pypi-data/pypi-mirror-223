from setuptools import find_packages, setup

with open("README.md", encoding="utf8") as f:
    readme = f.read()

setup(
    name="jupyterhub-datalaboauthenticator",
    version="1.0",
    description="Custom OAuthenticator for the Datalab",
    url="https://github.com/aidaph/datalaboauthenticator",
    author="Aida Palacio",
    author_email="aidaph@ifca.unican.es",
    long_description=readme,
    long_description_content_type="text/markdown",
    entry_points={
        # Thanks to this, user are able to do:
        #
        #     c.JupyterHub.authenticator_class = "tmp"
        #
        # ref: https://jupyterhub.readthedocs.io/en/4.0.0/reference/authenticators.html#registering-custom-authenticators-via-entry-points
        #
        "jupyterhub.authenticators": [
            "datalab-oauth = datalaboauthenticator.datalab:DatalabOAuthenticator",
        ],
    },
    packages=find_packages(),
    python_requires=">=3.8",
    install_require={
        "jupyterhub>=2.3.0",
        "oauthenticator",
        "traitlets",
    },
)
