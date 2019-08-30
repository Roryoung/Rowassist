"""rowassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse
from registration.backends.simple.views import RegistrationView

from RA import views
from RA.models import UserProfile
from RA.forms import registratonForm


class MyRegistrationView(RegistrationView):
	form_class = registratonForm

	def register(self, form_class):
		new_user = super(MyRegistrationView, self).register(form_class)
		new_user.first_name = form_class.cleaned_data['firstName']
		new_user.last_name = form_class.cleaned_data['lastName']
		new_user.save()

		user_profile = UserProfile()
		user_profile.user = new_user
		user_profile.save()
		return user_profile

	def get_form_class(self):
		return registratonForm

	def get_success_url(self, user):
		return reverse('joinClub')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),

    url(r'^club/join', views.joinClub, name='joinClub'),
    url(r'^club/create', views.createClub, name='createClub'),

    url(r'^accounts/register/$', MyRegistrationView.as_view(form_class=registratonForm), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
