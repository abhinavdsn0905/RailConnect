from django.shortcuts import render

# Create your views here.
from .models import Train
def train_list(request):
    trains = Train.objects.all()

    source = request.GET.get("source")
    destination = request.GET.get("destination")

    if source and destination:
        trains = Train.objects.filter(
            source__icontains=source,
            destination__icontains=destination
        )

    context = {
        "trains": trains
    }

    return render(request, "train_list.html", context)