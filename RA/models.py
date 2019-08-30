from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
	name = models.CharField(max_length=128, unique=True)
	shortName = models.CharField(max_length=128, unique=True)
	admins = models.ManyToManyField(User)

	def __str__(self):
		return self.name


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	club = models.ManyToManyField(Club, related_name="ApprovedClub")
	requestedClub = models.ManyToManyField(Club, related_name="RequestedClub")

	def __str__(self):
		return self.user.username


