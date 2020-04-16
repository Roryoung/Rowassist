from django.shortcuts import render
from rowassist.forms import UserForm, UserProfileForm, AccountForm, CreateSessionForm, CreateSessionIntervalForm, AddSessionEntryIntervalForm, AddSessionEntryForm
from rowassist.models import Athlete, Session, SessionEntry, SessionEntryInterval, SessionInterval
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rowassist.forms import UserForm, UserProfileForm, CreateClubForm, JoinClubForm
from rowassist.models import Club, Athlete, User
from rowassist.decorators import coach_requried
from django.http import JsonResponse
from django.forms.formsets import formset_factory


# Create your views here.

@login_required
def index(request):
    user_sessions = SessionEntry.objects.filter(athlete = request.user.athlete)
    context_dict = {'user_sessions': user_sessions}
    return render(request, 'rowassist/index.html', context_dict)


#------account views------
@login_required
def account(request):
    user = request.user
    user_sessions = SessionEntry.objects.filter(athlete=user.athlete)

    context_dict = {'user_sessions': user_sessions} 
    response = render(request, 'rowassist/account.html', context_dict)
    return response

def sign_in(request):
    error_message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('account'))
            else:
                error_message = "Your Rowassist account is disabled."
        else:
            error_message = "Invalid Username or Password."

    return render(request, 'rowassist/sign_in.html', {'error_message': error_message})


def sign_up(request):
    error_message = {}
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save the users data
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # save the extra data
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # log the new user in
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))


        else:
            error_message = {**user_form.errors, **profile_form.errors}
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rowassist/sign_up.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'error_message': error_message})


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


#------session views------
@login_required
def sessions(request):
    user = request.user
    club_sessions = Session.objects.filter(club=user.athlete.club)

    active_sessions = club_sessions.filter(isActive=True)
    previous_sessions = club_sessions.filter(isActive=False)

    context_dict = {'active_sessions': active_sessions, 'previous_sessions': previous_sessions}

    response = render(request, 'rowassist/sessions.html', context_dict)
    return response


@login_required
@coach_requried
def sessions_create(request):
    error_message = {}

    intervalFormSet = formset_factory(CreateSessionIntervalForm, min_num=1, extra=0)

    if request.method == 'POST':
        create_session_form = CreateSessionForm(data=request.POST)
        create_interval_form = intervalFormSet(data=request.POST)

        if create_session_form.is_valid() and create_interval_form.is_valid():
            session = create_session_form.save(commit=False)

            session.club = request.user.athlete.club
            session.save()

            if  create_session_form.data['type'] == 'V':
                for counter, intervalForm in enumerate(create_interval_form):
                    distance = intervalForm.cleaned_data.get('distance')
                    time = intervalForm.cleaned_data.get('time')
                    rest = intervalForm.cleaned_data.get('rest')
                    rate = intervalForm.cleaned_data.get('rate')

                    error_message = distance

                    if (intervalForm.is_valid()):
                        interval = intervalForm.save(commit=False)
                        interval.session = session
                        interval.intervalNo = counter
                        interval.save()

            return HttpResponseRedirect(reverse('sessions_create'))
        else:
            error_message = create_session_form.errors
            #error_message = {**create_session_form.errors, **create_interval_form.errors}

    return render(request, 'rowassist/sessions_create.html', {'sessionForm': CreateSessionForm(), 'intervalFormSet': intervalFormSet, 'error_message': error_message})

@login_required
@coach_requried
def sessions_close(request):
    sess_id = request.GET.get('id', '')
    session = Session.objects.get(id=sess_id)

    if (session.club == request.user.athlete.club):
        session.isActive = False
        session.save()

    return HttpResponseRedirect(reverse('sessions'))

@login_required
def sessions_edit(request):
    response = render(request, 'rowassist/sessions_edit.html')
    return response


@login_required
def sessions_view(request):
    sess_id = request.GET.get('id', '')
    target_session = Session.objects.get(id=sess_id)
    if (target_session.club == request.user.athlete.club):

        session_entries = SessionEntry.objects.filter(session=target_session)

        context_dict = {'session_entries': session_entries, 'target_session':target_session}

        response = render(request, 'rowassist/sessions_view.html', context=context_dict)
        return response

    return HttpResponseRedirect(reverse('account'))


@login_required
def sessions_view_interval(request):
    session_entry_id = request.GET.get('seid', '')
    session_entry = SessionEntry.objects.get(id=session_entry_id)
    if session_entry.session.club == request.user.athlete.club:
        session_entry_intervals = SessionEntryInterval.objects.filter(session_entry=session_entry)

        context_dict = {'intervals': session_entry_intervals}

        return render(request, 'rowassist/sessions_view_interval.html', context=context_dict)

    return HttpResponseRedirect(reverse('account')) 

@login_required
def sessions_enter(request):
    sess_id = request.GET.get("id", "")

    session = Session.objects.get(id=sess_id)
    user = request.user

    user_club = user.athlete.club

    if session.type != "V":
        interval_no = 1 if session.intervalNo is None else session.intervalNo
        distance_fixed = session.time is None
    else:
        session_intervals = SessionInterval.objects.filter(session=session)
        interval_no = len(session_intervals)

        distance_fixed = []

        for session_interval in session_intervals:
            distance_fixed.append(session_interval is None)

    intervalFormSet = formset_factory(AddSessionEntryIntervalForm, min_num=interval_no, max_num=interval_no, extra=0)

    error_message = ""

    if session.club != user_club:
        return HttpResponseRedirect(reverse('account'))
    else:
        if request.method == 'POST':
            interval_form = intervalFormSet(data=request.POST)
            if(interval_form.is_valid()):
                print(interval_form)
                session_entry = SessionEntry.objects.get_or_create(session = session, athlete=user.athlete)[0]
                for counter, intervalForm in enumerate(interval_form):
                    distance = intervalForm.cleaned_data.get('distance')
                    time = intervalForm.cleaned_data.get('time')
                    rate = intervalForm.cleaned_data.get('rate')

                    if(intervalForm.is_valid()):
                        interval = intervalForm.save(commit=False)
                        interval.session_entry = session_entry
                        interval.intervalNo = counter
                        interval.save()
                return HttpResponseRedirect(reverse('sessions'))
            else:
                error_message = interval_form.errors


    return render(request, 'rowassist/sessions_enter.html',
                  {'sessionForm': AddSessionEntryForm(), 'intervalFormSet': intervalFormSet,
                   'session': session,
                   'error_message': error_message, 'interval_no': interval_no,
                   'distance_fixed': distance_fixed})


@login_required
@coach_requried
def create_club(request):
    error_message = {}
    create_club_form = CreateClubForm()

    if request.method == 'POST':
        club_form = CreateClubForm(data=request.POST)

        if club_form.is_valid():
            # save new club
            club_form.save(commit=True)

            # update curent user's club
            name = club_form.data['name']
            request.user.athlete.club = Club.objects.get(name=name)
            request.user.athlete.save()

            # return user to account page
            return HttpResponseRedirect(reverse('account'))
        else:
            error_message = club_form.errors

    return render(request, 'rowassist/create_club.html', {'form': create_club_form, 'error_message': error_message})

#------Club views------
@login_required
def club(request):
    context_dict = {}
    club = request.user.athlete.club
    if club:
        context_dict['club'] = club
        context_dict['coaches'] = Athlete.objects.filter(is_coach = True, club=club)
        context_dict['athletes'] = Athlete.objects.filter(is_coach = False, club=club)

        return render(request, 'rowassist/club.html', context_dict)
    else:
        if request.user.athlete.requested_club:
            return HttpResponseRedirect(reverse('join_club_confirm')) 
        return HttpResponseRedirect(reverse('join_club')) 

@login_required
def join_club(request):
    form = JoinClubForm()
    if request.method == 'POST':
        form = JoinClubForm(data=request.POST)

        if form.is_valid():
            club = form.data['club']
            request.user.athlete.requested_club = Club.objects.get(name=club)
            request.user.athlete.save()

            return HttpResponseRedirect(reverse('join_club_confirm'))

    clubs = Club.objects.filter()
    return render(request, 'rowassist/join_club.html', {'clubs': clubs, 'form': form})


@login_required
def join_club_confirm(request):
    club = request.user.athlete.requested_club.name
    return render(request, 'rowassist/join_club_confirm.html', {'club': club})


@login_required
def join_club_cancel(request):
    user = request.user
    if user.athlete.requested_club != None:
        user.athlete.requested_club = None
        user.athlete.save()

        return HttpResponseRedirect(reverse('account'))

    return HttpResponseRedirect(reverse('join_club'))


@login_required
def leave_club(request):
    return render(request, 'rowassist/leave_club.html')


@login_required
def leave_club_confirm(request):
    athlete = request.user.athlete
    athlete.club = None
    athlete.save()
    return HttpResponseRedirect(reverse('account'))


@login_required
@coach_requried
def approve_member(request):
    coaches = Athlete.objects.filter(requested_club=request.user.athlete.club, is_coach=True)
    athletes = Athlete.objects.filter(requested_club=request.user.athlete.club, is_coach=False)

    response = render(request, 'rowassist/approve_member.html', {'coaches': coaches, 'athletes': athletes})
    return response


@login_required
@coach_requried
def approve_member_accept(request):
    if request.method == 'POST' and request.is_ajax():
        user = User.objects.get(username=request.POST['username'])
        athletes = Athlete.objects.get(user=user)
        athletes.club = athletes.requested_club
        athletes.requested_club = None
        athletes.save()

        data = {
            'worked': True,
        }
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(reverse('approve_member'))


@login_required
@coach_requried
def approve_member_reject(request):
    if request.method == 'POST' and request.is_ajax():
        user = User.objects.get(username=request.POST['username'])
        athletes = Athlete.objects.get(user=user)
        athletes.requested_club = None
        athletes.save()

        data = {
            'worked': True,
            'first_name': user.username,
            'last_name': user.last_name,
        }

        return JsonResponse(data)
    else:
        return HttpResponseRedirect(reverse('approve_member'))
