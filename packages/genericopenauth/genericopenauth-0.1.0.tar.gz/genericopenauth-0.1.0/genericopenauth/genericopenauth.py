from jupyterhub.traitlets import Callable
from traitlets import Unicode, Union
from oauthenticator.generic import  GenericOAuthenticator
import os
import jwt

class CustomGenericOAuthenticator(GenericOAuthenticator):
    groups_claim = Union(
        [Unicode(os.environ.get('OAUTH2_GROUPS_CLAIM', 'groups')), Callable()],
        config=True,
        help="""
        Name of the claim inside jwt (access) token referring to the groups the 
        user belongs to. Since groups are not part of user info coming from user 
        data api this is some kind of workaround for reading groups from identity provider.
        """,
    )
    async def update_auth_model(self, auth_model):
        """
        Overridden to collect information about groups from jwt (access) 
        token and inject it to auth_model. 

        Called by the :meth:`oauthenticator.OAuthenticator.authenticate`
        """
        auth_state = auth_model["auth_state"]
        if auth_state and auth_state["access_token"]:
            access_token = auth_state["access_token"]
            decoded_data = jwt.decode(jwt=access_token, options={"verify_signature": False})
            groups = decoded_data.get(self.groups_claim, [])
            auth_model["groups"] = groups
        return auth_model