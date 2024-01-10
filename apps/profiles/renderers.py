import json
from rest_framework.renderers import JSONRenderer

# JSONRenders render the request data into JSON, using utf-8 encoding.
class ProfileJSONRenderer(JSONRenderer):
    charset = "utf-8"

    # method that overides JSONRenderer to render data under a profile namespace
    def render(self, data, accepted_media_type=None, renderer_context=None):
        errors = data.get("errors", None)
        
        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)
        return json.dumps({"profile": data})
    