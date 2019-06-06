from django.http import HttpResponseRedirect
from django.views import View

class HomeRedirectView(View):
    """
    Redirect backoffice's home to admin's login
    """
    def get(self, request):
        return HttpResponseRedirect('myadmin/')