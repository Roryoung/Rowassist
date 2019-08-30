from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from RA.models import UserProfile, Club
from RA.forms import joinClubForm, createClubForm

# Create your views here.
def index(request):
	return render(request, 'index.html')

def joinClub(request):
	if request.method == 'POST':
		form =joinClubForm(data=request.POST)

		if form.is_valid():
			id = form.data['requestedClub']
			request.user.userprofile.requestedClub.add(Club.objects.get(id=id))
			request.user.userprofile.save()

			return HttpResponseRedirect(reverse('index'))

	context_dict = {}
	context_dict['form'] = joinClubForm()
	context_dict['clubs'] = Club.objects.filter()

	return render(request, 'club/join_club.html', context_dict)

def createClub(request):
	if request.method == 'POST':
		form = createClubForm(data=request.POST)
		if form.is_valid():
			club = form.save(commit = True)
			club.admins.add(request.user)
			club.save()

			name = form.data['name']
			request.user.userprofile.club.add(Club.objects.get(name=name))
			request.user.userprofile.save()



			return HttpResponseRedirect(reverse('index'))
		else:
			print(form.errors)
	form = createClubForm()
	return render(request, 'club/create_club.html', {'form': form})
