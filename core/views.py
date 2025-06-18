from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import CommandForm
import subprocess

def login_view(request):
    return render(request, 'registration/login.html')


@login_required
def command_view(request):
    output = ''
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            cmd = form.cleaned_data['command']
            try:
                # Safely execute the command
                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = result.stdout or result.stderr
            except Exception as e:
                output = str(e)
    else:
        form = CommandForm()

    return render(request, 'core/command_form.html', {'form': form, 'output': output})



