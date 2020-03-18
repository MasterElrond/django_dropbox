from django.test import SimpleTestCase, Client, override_settings
from django.conf import settings

from dropbox import Dropbox

# @override_settings(DROPBOX_CLIENT_SECRET='test_client_secret')
class Test(SimpleTestCase):
    def test_verification_challenge(self):
        pass

    def test_signature_verification(self):
        pass

    def test_dbx(self):
        dbx = Dropbox(settings.DROPBOX_ACCESS_TOKEN)
        result = dbx.files_list_folder(path='/roasts')
        print(result)

        # print(dir(dbx))
