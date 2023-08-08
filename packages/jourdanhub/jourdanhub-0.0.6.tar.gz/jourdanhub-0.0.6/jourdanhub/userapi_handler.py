
from jupyterhub.apihandlers.base import APIHandler
from tornado import web
import json


class SelfAPIHandler(APIHandler):
    """
        Handler for the user api endpoint.
        This allows us to force the visibility of the auth state


        Return the authenticated user's model
        Based on the authentication info. Acts as a 'whoami' for auth tokens.
    """

    """Return the authenticated user's model

    Based on the authentication info. Acts as a 'whoami' for auth tokens.
    """

    async def get(self):
        user = self.current_user
        if user is None:
            raise web.HTTPError(403)

        get_model = self.user_model

        """
        _added_scopes = set()
        if isinstance(user, orm.Service):
            # ensure we have the minimal 'identify' scopes for the token owner
            dentify_scopes = scopes.identify_scopes(user)
            get_model = self.service_model
        else:
            identify_scopes = scopes.identify_scopes(user.orm_user)
            get_model = self.user_model

        

        # ensure we have permission to identify ourselves
        # all tokens can do this on this endpoint
        for scope in identify_scopes:
            if scope not in self.expanded_scopes:
                _added_scopes.add(scope)
                self.expanded_scopes |= {scope}
        if _added_scopes:
            # re-parse with new scopes
            self.parsed_scopes = scopes.parse_scopes(self.expanded_scopes)

        """

        model = get_model(user)

        # add session_id associated with token
        # added in 2.0
        token = self.get_token()
        if token:
            model["session_id"] = token.session_id
        else:
            model["session_id"] = None

        # add scopes to identify model,
        # but not the scopes we added to ensure we could read our own model
        #model["scopes"] = sorted(self.expanded_scopes.difference(_added_scopes))
        model["scopes"] = sorted(self.expanded_scopes)

        model["jourdan"] = "teste"
        self.write(json.dumps(model))