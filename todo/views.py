from django.shortcuts import render

from .models import ToDo


def index(request):
    
    if request.method == "POST":
        print("POST")
        text = request.POST.get("text", None)
        print("TEXT", text)
        if text:
            print("SAVE")
            ToDo.objects.create(
                text=text
            )

    todo = ToDo.objects.all()

    return render(request, "index.html", {"todo": todo})