import time
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from apps.diplomas.models import Assertion
from apps.utils.utils import custom_email


class IndexRedirectView(View):
    """
    Redirect backoffice's home to admin's login
    """
    def get(self, request):
        return HttpResponseRedirect('myadmin/')

class SendEmail(View):
    """
    Web pages to send notifications
    """
    def get(self, request):

        assertions = Assertion.objects.filter(sent=False).exclude(short_url=' ')

        from_email = 'no-reply@diplofy.com'
        html_template = get_template('diplomas/diploma_notification.html')
        aux = 0

        for asserttion in assertions:

            #if settings.DEBUG is True and aux == 2:
            #    aux = 0
            #    time.sleep(settings.EMAIL_SLEEP)

            subject = asserttion.diploma.event.issuer.name + ' te envió un diploma digital por haber participado del curso ' + asserttion.diploma.event.name
                    
            to_email = asserttion.recipient.email

            ctx = { 
                'first_name': asserttion.recipient.first_name,
                'issuer': asserttion.diploma.event.issuer.name,
                'issuer_url': asserttion.diploma.event.issuer.url,
                'diploma': asserttion.diploma.event.name,
                'diploma_url': asserttion.diploma.event.url,
                'licence': asserttion.licence,
                'issued_on': asserttion.issued_on,
                'expires': '' if asserttion.expires == None else asserttion.expires,
                'assertion_url': asserttion.short_url
            }            

            email = custom_email(subject, from_email, to_email, html_template, ctx)

            if email:
                asserttion.sent = True
                asserttion.save()
            else:  
                pass

            aux = aux + 1
        
        return HttpResponse("Here's the text of the Web page.")