from django.shortcuts import render, redirect
from .forms import InfoForm
from .models import Info, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# @method_decorator(login_required, name='dispatch')
class ProfileCreate(CreateView):
    fields = ['name', 'description', 'age']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/profile/' + str(self.object.pk))

def login_view(request):
     # if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect.')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def dashboard(request):
    form = InfoForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            info = form.save(commit=False)
            info.user = request.user
            info.save()
            return redirect("parenTotutor:dashboard")

    followed_info = Info.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(
        request,
        "dashboard.html",
        {"form": form, "intp": followed_info},
    )


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "parenTotutor/profile_list.html", {'profiles': profiles})


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "profile.html", {'profile': profile})

   @login_required
def profile(request, username):
  user = User.objects.get(username=username)
  profiles = list(Profile.objects.filter(user=user))

  return render(request, 'profile.html', { 'username': username, 'profile': profile})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
            else:
                print('The username and/or password is incorrect.')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
          return render(request, 'signup.html', {'form': form })
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form })

