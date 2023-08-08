import jupyterhub.apihandlers.users as users
from jupyterhub import app
from .userapi_handler import SelfAPIHandler
import sys
import os
import datetime

handlers_map = {
    users.SelfAPIHandler: SelfAPIHandler
}


class JourdanHub(app.JupyterHub):
    def init_handlers(self):
        super().init_handlers()
        for i, cur_handler in enumerate(self.handlers):
            new_handler = handlers_map.get(cur_handler[1])
            if new_handler:
                cur_handler = list(cur_handler)
                cur_handler[1] = new_handler
                self.handlers[i] = tuple(cur_handler)

main = JourdanHub.launch_instance