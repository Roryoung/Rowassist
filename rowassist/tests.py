from django.test import TestCase
from django.contrib.auth.models import User
from rowassist.models import Athlete, Club
from django.urls import reverse


class SimpleTest(TestCase):

    def setUp(self):
        normal_non_club_user = User.objects.create_user('temp_nonclub', 'temp_nonclub@gmail.com', 'temp_nonclub')
        normal_user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        coach_user = User.objects.create_user('temp_coach', 'coach@gmail.com', 'temp_coach')

        self.club = Club.objects.create(name="TestClub", short_name="TC", url="http://testclub.com/")

        nonclub_athlete = Athlete.objects.create(user=normal_non_club_user, is_coach=False, picture=None, club=None, requested_club=self.club)
        athlete = Athlete.objects.create(user=normal_user, is_coach=False, picture=None, club=self.club)
        coach_athlete = Athlete.objects.create(user=coach_user, is_coach=True, picture=None, club=self.club)

    # Tests signin functionality & secure page for logged in user
    def test_secure_page(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse("account"), follow=True)
        user = User.objects.get(username='temporary')
        self.assertEqual(response.context['user'].email, 'temporary@gmail.com')

    # Tests coach functionality & secure coach access
    def test_secure_coach_page(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse("sessions_create"), follow=True)
        user = User.objects.get(username='temporary')
        self.assertEqual(response.context.get('sessionForm'), None)

    # Tests coach functionality & secure coach access
    def test_secure_coach_page_as_coach(self):
        self.client.login(username='temp_coach', password='temp_coach')
        response = self.client.get(reverse("sessions_create"), follow=True)
        user = User.objects.get(username='temp_coach')
        self.assertNotEqual(response.context.get('sessionForm'), None)

    # # Tests join club
    # def test_join_club(self):
    #     self.client.login(username='temp_nonclub', password='temp_nonclub')
    #     response = self.client.get(reverse("account"), follow=True)
    #     user = User.objects.get(username='temp_nonclub')
    #     self.assertEqual(response.context['user'].athlete.club, None)

    # # Tests join club 2
    # def test_join_club_2(self):
    #     self.client.login(username='temp_nonclub', password='temp_nonclub')
    #     response = self.client.get(reverse("account"), follow=True)
    #     user = User.objects.get(username='temp_nonclub')
    #     user.club = self.club
    #     self.assertEqual(response.context['user'].athlete.club, self.club)
