from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import LiveStream, Comment
from django.utils import timezone

@login_required
def create_stream(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        stream = LiveStream.objects.create(
            title=title,
            description=description,
            streamer=request.user,
            start_time=timezone.now()
        )
        return redirect('stream_detail', stream_id=stream.id)
    return render(request, 'livestream/create_stream.html')

@login_required
def stream_detail(request, stream_id):
    stream = LiveStream.objects.get(id=stream_id)
    comments = Comment.objects.filter(stream=stream).order_by('-created_at')
    context = {
        'stream': stream,
        'comments': comments
    }
    return render(request, 'livestream/stream_detail.html', context)

@login_required
def end_stream(request, stream_id):
    if request.method == 'POST':
        stream = LiveStream.objects.get(id=stream_id)
        if request.user == stream.streamer:
            stream.end_time = timezone.now()
            stream.is_active = False
            stream.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
def add_comment(request, stream_id):
    if request.method == 'POST':
        stream = LiveStream.objects.get(id=stream_id)
        content = request.POST.get('content')
        Comment.objects.create(
            user=request.user,
            stream=stream,
            content=content
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def stream_list(request):
    active_streams = LiveStream.objects.filter(is_active=True).order_by('-start_time')
    context = {
        'streams': active_streams
    }
    return render(request, 'livestream/stream_list.html', context)







