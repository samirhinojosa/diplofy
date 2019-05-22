from apps.utils.admin import DiplofyAdminSite
from .models import Issuer, Diploma, Event, Tag, Recipient, Assertion
from .admins.issuers import IssuerAdmin
from .admins.tags import TagAdmin
from .admins.events import EventAdmin
from .admins.diplomas import DiplomaAdmin
from .admins.assertions import AssertionAdmin
from .admins.recipients import RecipientAdmin


#Diplofy's admin customed
diplofy_admin_site = DiplofyAdminSite(name='diplofy_admin')

diplofy_admin_site.register(Assertion, AssertionAdmin)
diplofy_admin_site.register(Recipient, RecipientAdmin)
diplofy_admin_site.register(Tag, TagAdmin)
diplofy_admin_site.register(Event, EventAdmin)
diplofy_admin_site.register(Diploma, DiplomaAdmin)
diplofy_admin_site.register(Issuer, IssuerAdmin)