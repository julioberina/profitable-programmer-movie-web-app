from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
             'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://abqpride.com/wp-content/uploads/2017/01/no-image-available.png'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
            response = AT.insert(data)
            messages.success(request, 'New Movie Added: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Error encountered creating movie: {}'.format(e))

    return redirect('/')

def update(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'http://abqpride.com/wp-content/uploads/2017/01/no-image-available.png'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
            response = AT.update(movie_id, data)
            messages.info(request, 'Updated Movie: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Error encountered updating movie: {}'.format(e))

    return redirect('/')

def delete(request, movie_id):
    try:
        name = AT.get(movie_id)['fields']['Name']
        AT.delete(movie_id)
        messages.error(request, 'Deleted Movie: {}'.format(name))
    except Exception as e:
        messages.warning(request, 'Error encountered deleting movie: {}'.format(e))

    return redirect('/')
