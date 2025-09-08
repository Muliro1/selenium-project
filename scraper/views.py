from django.shortcuts import render
from django.http import JsonResponse
from .scraper import run_demo_scrape


def home(request):
    return render(request, 'scraper/home.html')


def run_scrape_view(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)
    try:
        result = run_demo_scrape()
        return JsonResponse(result)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)


def scrape_github_view(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)
    try:
        result = scrape_github_trending()
        return JsonResponse(result)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)
