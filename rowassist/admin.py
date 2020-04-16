from django.contrib import admin
from rowassist.models import Athlete, Club, Session, SessionInterval, SessionEntry, SessionEntryInterval

# Register your models here.
admin.site.register(Athlete)
admin.site.register(Club)
admin.site.register(Session)
admin.site.register(SessionInterval)
admin.site.register(SessionEntry)
admin.site.register(SessionEntryInterval)