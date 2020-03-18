import json

from django.views import View
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from .utils import timesafe_mac_compare

data = "{'f':df}"
def test(r):
    json.loads(data)
    return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class SimpleDropboxView(View):
    """https://www.dropbox.com/developers/reference/webhooks"""

    @staticmethod
    def _get_client_secret():
        return settings.DROPBOX_CLIENT_SECRET

    def get(self, request):
        """webhook initial verification"""
        try:
            challenge = request.GET['challenge']
        except KeyError:
            raise SuspicousOperation()

        response = HttpResponse(challenge, content_type='text/plain')
        response['X-Content-Type-Options'] = 'nosniff'
        return response

    def post(self, request):
        """webhook signature verification"""

        signature = request.headers.get('X-Dropbox-Signature')

        if not timesafe_mac_compare(signature, self._get_client_secret(), self.request.body):
            raise PermissionDenied()

        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            raise SuspiciousOperation()

        self.callback(data)
        return HttpResponse(status=204)

    @staticmethod
    def callback(data):
        """Entrypoint for task creation"""
        raise NotImplementedError
