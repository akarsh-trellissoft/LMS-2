from django.contrib import admin
from .models import *
from .manager import *

admin.site.register(Leave)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(MailingGroup)
admin.site.register(Nationality)
admin.site.register(Religion)
admin.site.register(Employee)
# admin.site.register(Bank)
# admin.site.register(Emergency)
# admin.site.register(Relationship)