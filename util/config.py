import json
import os


class config:

    def recuperar(self, nome):
        return json.load(open(os.path.join(os.path.dirname(os.pardir), "config.json")))[nome]
