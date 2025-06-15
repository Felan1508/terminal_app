# core/views.py
from django.shortcuts import render
import subprocess

def terminal_view(request):
    output = ""
    if request.method == "POST":
        command = request.POST.get("command")
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)
    return render(request, "core/command_form.html", {"output": output})
