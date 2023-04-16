from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import TemplateView
import requests, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import People, Starships, Planets, Profile, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import random
from .forms import CommentForm, UserSearchForm
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    return redirect ('/login')


@login_required
def dashboard(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    people = People.objects.filter(user=current_user).values_list('name', flat=True)
    starships = Starships.objects.filter(user=current_user).values_list('name', flat=True)
    planets = Planets.objects.filter(user=current_user).values_list('name', flat=True)
    
    context = {
        'people': list(people),
        'starships': list(starships),
        'planets': list(planets),
        'profile' : profile
    }
    
    latest_person_query = People.objects.filter(user=current_user)
    if len(latest_person_query) > 0:
        latest_person = latest_person_query.latest("created_at")
    else:
        latest_person = ''
    latest_starship_query = Starships.objects.filter(user=current_user)
    if len(latest_starship_query) > 0:
        latest_starship = latest_starship_query.latest('created_at')
    else:
        latest_starship = ''
    latest_planet_query = Planets.objects.filter(user=current_user)
    if len(latest_planet_query) > 0:
        latest_planet = latest_planet_query.latest('created_at')
    else:
        latest_planet = ''
        
    late = {
        'latest_person': latest_person,
        'latest_starship': latest_starship,
        'latest_planet': latest_planet,
    }
    print(context)
    print(late)
    return render(request, 'dashboard.html',  {'context': context, 'late': late})


class RollPage(TemplateView):
    template_name = 'roll.html'


@api_view(['POST'])
def RollAPIView(request):
    if request.method == 'POST':
        endpoints = request.data.get('endpoints', [])
        results = []
        for endpoint in endpoints:
            response = requests.get(endpoint).json()
            result = {}
            if endpoint.endswith('people/'):
                random_person = response['results'][random.randint(0, len(response['results']) - 1)]
                result = {
                    'type': 'people',
                    'name': random_person['name'],
                    'hair_color': random_person['hair_color'],
                    'gender': random_person['gender']
                }
            elif endpoint.endswith('starships/'):
                random_ship = response['results'][random.randint(0, len(response['results']) - 1)]
                result = {
                    'type': 'starship',
                    'name': random_ship['name'],
                    'manufacturer': random_ship['manufacturer'],
                    'model': random_ship['model']
                }
            elif endpoint.endswith('planets/'):
                random_planet = response['results'][random.randint(0, len(response['results']) - 1)]
                result = {
                    'type': 'planet',
                    'name': random_planet['name'],
                    'population': random_planet['population'],
                    'terrain': random_planet['terrain']
                }
            results.append(result)
        return Response({'results': results})
    return Response({'message': 'Invalid Request'})




@login_required
@csrf_exempt
def store_items(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)  # parse the JSON string
        results = data.get('results', [])
        saved_items = []
        for result in results:
            item_type = result['type']
            item_name = result['name']
            item_in_db = False

            # Check if item exists in database for each type
            if item_type == 'people':
                if People.objects.filter(name=item_name).exists():
                    item_in_db = True
            elif item_type == 'planet':
                if Planets.objects.filter(name=item_name).exists():
                    item_in_db = True
            elif item_type == 'starship':
                if Starships.objects.filter(name=item_name).exists():
                    item_in_db = True

            # Save item if not in database
            if not item_in_db:
                if item_type == 'people':
                    People.objects.create(name=item_name, hair_color=result['hair_color'], gender=result['gender'], user=request.user)
                elif item_type == 'planet':
                    Planets.objects.create(name=item_name, population=result['population'], terrain=result['terrain'], user=request.user)
                elif item_type == 'starship':
                    Starships.objects.create(name=item_name, manufacturer=result['manufacturer'], model=result['model'], user=request.user)
                saved_items.append(result)
                print(saved_items)

        return JsonResponse({'message': 'Items saved successfully.', 'saved_items': saved_items}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def profile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    count_1 = People.objects.filter(user=profile.user).count()
    count_2 = Starships.objects.filter(user=profile.user).count()
    count_3 = Planets.objects.filter(user=profile.user).count()

    total =  {
        'total' : count_1 + count_2 + count_3
    }
    
    people = People.objects.filter(user=profile.user).values_list('name', flat=True)
    starships = Starships.objects.filter(user=profile.user).values_list('name', flat=True)
    planets = Planets.objects.filter(user=profile.user).values_list('name', flat=True)
    
    items = {
        'people': list(people),
        'starships': list(starships),
        'planets': list(planets)
    }
    form = CommentForm()
    profile_id = profile.id
    comments = Comment.objects.filter(profile=profile).order_by('-created_at')
    context = {
        'items': items,
        'total' : total,
        'form': form,
        'profile_id': profile_id,
        'comments': comments,
        'profile': profile,
    }
    
    return render(request, 'profile.html', context)


@login_required
def add_comment(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print('test form submitted')
        if form.is_valid():
            print('test form made it?')
            comment = Comment(content=form.cleaned_data['content'], profile=profile, user=request.user)
            comment.save()
            print(comment)
            return redirect(f'/profile/{pk}')
    else:
        form = CommentForm()

    return redirect(f'/profile/{pk}')

@login_required
def delete_comment(request, profile_id, comment_id):
    comment = Comment.objects.filter(id=comment_id, user=request.user).first()
    if request.method == 'POST' and comment:
        comment.delete()
        print('Comment deleted')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def edit_comment(request, profile_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user != request.user:
        return JsonResponse({'error': 'You are not authorized to edit this comment.'})
    content = request.POST.get('content')
    if not content:
        return JsonResponse({'error': 'Comment content is required.'})
    comment.content = content
    comment.save()
    return JsonResponse({'success': 'Comment updated successfully.'})


def user_search(request):
    form = UserSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('search_query', '')
        results = User.objects.filter(username__icontains=query)
        profiles = Profile.objects.filter(user__in=results)
        
    else:
        results = User.objects.all()
        profiles = Profile.objects.all()
    return render(request, 'search.html', {'form': form, 'results': results, 'profiles': profiles})


def about(request):
    pass

    return render(request, 'about.html')