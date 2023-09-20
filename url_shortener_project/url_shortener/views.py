from django.shortcuts import render, redirect
from .models import URL
import random
import string

def shorten_url(request):
    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        if long_url:
            # Check if the long URL is already in the database
            try:
                url = URL.objects.get(long_url=long_url)
                short_url = url.short_url
            except URL.DoesNotExist:
                # Generate a new short URL and save it to the database
                short_url = generate_short_url()
                URL.objects.create(long_url=long_url, short_url=short_url)

            return render(request, 'shortened.html', {'short_url': short_url, 'long_url': long_url})
        else:
            return render(request, 'index.html', {'error': 'Please enter a URL to shorten'})

def redirect_to_long_url(request, short_url):
    try:
        url = URL.objects.get(short_url=short_url)
        return redirect(url.long_url)
    except URL.DoesNotExist:
        return render(request, '404.html')
