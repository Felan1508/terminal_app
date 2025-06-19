import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

BASE_DIR = settings.BASE_DIR  # current project dir

def list_files(request):
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    return render(request, 'file_manipulator/list_files.html', {'files': files})

def edit_file(request, filename):
    filepath = os.path.join(BASE_DIR, filename)

    if request.method == 'POST':
        content = request.POST.get('content', '')
        with open(filepath, 'w') as f:
            f.write(content)
        return HttpResponseRedirect('/')

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        content = f"Error reading file: {e}"

    return render(request, 'file_manipulator/edit_file.html', {'filename': filename, 'content': content})
