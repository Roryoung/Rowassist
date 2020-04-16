from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Club(models.Model):
	name = models.CharField(max_length=128, unique=True)
	url = models.URLField(blank=True, null=True)
	short_name = models.CharField(max_length=128, unique=True)
    
	def __str__(self): # For Python 2, use __unicode__ too
		return self.name


class Athlete(models.Model):
	user = models.OneToOneField(User)
	is_coach = models.BooleanField()
	User._meta.get_field('email')._unique = True
	picture = models.ImageField(upload_to='profile_images', blank=True)
	club = models.ForeignKey(Club, blank = True, null = True, on_delete=models.SET_NULL, related_name="ApprovedClub")
	requested_club = models.ForeignKey(Club, blank = True, null = True, on_delete=models.SET_NULL, related_name="RequestedClub")


	#def save(self, *args, **kwargs):
	#	self.slug = slugify(self.email)
	#	super(Category, self).save(*args, **kwargs)
	
	class Meta:
		verbose_name_plural = 'athletes'

	def __str__(self): # For Python 2, use __unicode__ too
		return self.user.get_username()		

	def fullname(self):
		return self.user.first_name + " " + self.user.last_name
		

class Session(models.Model):
	types = (
		('S', 'Single interval'),
		('F', 'Fixed interval'),
		('V', 'Variable interval'),
	)
	club = models.ForeignKey(Club)
	type = models.CharField(max_length=1, choices=types)  # enum
	date = models.DateField()
	description = models.TextField(blank=True, null=True)
	name = models.TextField()

	distance = models.IntegerField(blank=True, null=True)
	time = models.TimeField(blank=True, null=True)
	rate = models.IntegerField(blank=True, null=True)
	rest = models.TimeField(blank=True, null=True)
	intervalNo = models.IntegerField(blank=True, null=True)

	isActive = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	
	
class SessionInterval(models.Model):
	session = models.ForeignKey(Session)
	intervalNo = models.IntegerField(primary_key=True)

	distance = models.IntegerField(blank=True, null=True)
	time = models.TimeField(blank=True, null=True)
	rate = models.IntegerField(blank=True, null=True)
	rest = models.TimeField(blank=True, null=True)

	class Meta:
		unique_together = (('session', 'intervalNo'),)

	def __str__(self):
		return self.session.name + ", " +  str(self.intervalNo)

class SessionEntry(models.Model):
	session = models.ForeignKey(Session, blank=False, null=False)
	athlete = models.ForeignKey(Athlete, blank=False, null=False)

	types = (
		('S', 'Single interval'),
		('F', 'Fixed interval'),
		('V', 'Variable interval'),
	)
	type = models.CharField(max_length=1, choices=types)  # enum
	date = models.DateField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	name = models.TextField(blank=True, null=True)
	
	distance = models.IntegerField(blank=True, null=True)
	time = models.TimeField(blank=True, null=True)
	rate = models.IntegerField(blank=True, null=True)
	rest = models.TimeField(blank=True, null=True)
	intervalNo = models.IntegerField(blank=True, null=True)


	def __str__(self):
		return self.session.name + ", " + self.athlete.user.first_name
	
	
class SessionEntryInterval(models.Model):
	session_entry = models.ForeignKey(SessionEntry)
	intervalNo = models.IntegerField(primary_key=True)

	distance = models.PositiveIntegerField(blank=True, null=True)  # in metres
	time = models.DurationField(blank=True, null=True)
	strokes_per_minute = models.PositiveIntegerField(blank=True, null=True)
	rest = models.TimeField(blank=True, null=True)

	
	class Meta:
		unique_together = (('session_entry', 'intervalNo'),)

	def __str__(self):
		return self.session_entry.session.name + ", " +  str(self.intervalNo)
