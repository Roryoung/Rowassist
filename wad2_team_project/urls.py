"""wad2_team_project URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
#
from rowassist import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    url(r'^admin/', admin.site.urls),
	
    url(r'^$', views.index, name='index'),

    url(r'^account/$', views.account, name='account'),
    url(r'^account/sign_in/$', views.sign_in, name='sign_in'),
    url(r'^account/sign_up/$', views.sign_up, name='sign_up'),
    url(r'^account/sign_out/$', views.sign_out, name='sign_out'),

    url(r'^sessions/$', views.sessions, name='sessions'),
    url(r'^sessions/create/$', views.sessions_create, name='sessions_create'),
    url(r'^sessions/close/$', views.sessions_close, name='sessions_close'),
    url(r'^sessions/edit/$', views.sessions_edit, name='sessions_edit'),
    url(r'^sessions/view/$', views.sessions_view, name='sessions_view'),
    url(r'^session/view/interval/$', views.sessions_view_interval, name="sessions_view_interval"),
    url(r'^sessions/view/enter/$', views.sessions_enter, name='sessions_enter'),

    url(r'^club/$', views.club, name='club'),
    url(r'^club/create/$', views.create_club, name='create_club'),
    url(r'^club/join/$', views.join_club, name='join_club'),
    url(r'^club/join/confirm/$', views.join_club_confirm, name='join_club_confirm'),
    url(r'^club/join/cancel/$', views.join_club_cancel, name='join_club_cancel'),
    url(r'^club/leave/$', views.leave_club, name='leave_club'),
    url(r'^club/leave/confirm$', views.leave_club_confirm, name='leave_club_confirm'),
    url(r'^club/approve_member/$', views.approve_member, name='approve_member'),
    url(r'^club/approve_member/accept$', views.approve_member_accept, name='approve_member_accept'),
    url(r'^club/approve_member/reject$', views.approve_member_reject, name='approve_member_reject'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
