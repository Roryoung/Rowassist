from django.conf.urls import url
from rowassist import views

urlpatterns = [
	url(r'^$', views.home, name='index'),

	url(r'^account/$', views.account, name='account'),
	url(r'^account/sign_in/$', views.sign_in, name='sign_in'),
	url(r'^account/sign_up/$', views.sign_up, name='sign_up'),
	url(r'^account/sign_out/$', views.sign_out, name='sign_out'),
	url(r'^account/sessions/$', views.account_sessions, name='account_sessions'),
	url(r'^account/statistics/$', views.account_statistics, name='account_statistics'),

	url(r'^sessions/$', views.sessions, name='sessions'),
	url(r'^sessions/create/$', views.sessions_create, name='sessions_create'),
	url(r'^sessions/close/$', views.sessions_close, name='sessions_close'),
	url(r'^sessions/edit/$', views.sessions_edit, name='sessions_edit'),
	url(r'^sessions/view/$', views.sessions_view, name='sessions_view'),
	url(r'^session/view/interval/$', views.sessions_view_interval, name="sessions_view_interval"),
	url(r'^sessions/view/enter/$', views.sessions_enter, name='sessions_enter'),


	url(r'^club/create/$', views.create_club, name='create_club'),
	url(r'^club/join/$', views.join_club, name='join_club'),
	url(r'^club/join/confirm/$', views.join_club_confirm, name='join_club_confirm'),
	url(r'^club/join/cancel/$', views.join_club_cancel, name='join_club_cancel'),
	url(r'^club/leave/$', views.leave_club, name='leave_club'),
	url(r'^club/leave/confirm$', views.leave_club_confirm, name='leave_club_confirm'),
	url(r'^club/approve_member/$', views.approve_member, name='approve_member'),
	url(r'^club/approve_member/accept$', views.approve_member_accept, name='approve_member_accept'),
	url(r'^club/approve_member/reject$', views.approve_member_reject, name='approve_member_reject'),


]