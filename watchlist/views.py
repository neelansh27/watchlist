from django.shortcuts import render
from .models import List, UserProfile
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        # print('hi')
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

    else:
        form = RegistrationForm()
    return render(request, 'watchlist/signup.html', {
            'form': form
        })

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/watchlist/')
@login_required(login_url='/watchlist/login')
def index(request):
    if request.method == 'POST':
        print('hi')
        try:
            movie_name = request.POST['movieName'].title()
            platform_name = request.POST['platformName'].title()
            author = request.user
            print('author'+ str(author))
            entry = List(movie_name=movie_name, platform_name=platform_name)
            print(entry)
            entry.save()
            # problematic
            user_profile = UserProfile.objects.create(user=author)
            print(user_profile)
            user_profile.items.add(entry)
            user_profile.save()
            print(user_profile.items.all())

            # print(f"{movie_name} streaming on {platform_name}")

        except:
            movie_id = request.POST['movie_id']
            # print(movie_id)
            movie = List.objects.get(pk=movie_id)
            if movie:
                movie.delete()
            else:
                pass

        finally:
            return HttpResponseRedirect(reverse('index'))

    elif request.method == 'GET':
        try:
            current_user = request.user.username
            print(current_user)
            movies = current_user.items.all()
            print(movies)
        except:
            return render(request, 'watchlist/index.html')
        else:
            return render(request, 'watchlist/index.html', {
            'movies': movies
            })
