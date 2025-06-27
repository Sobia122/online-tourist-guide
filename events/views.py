from datetime import datetime
from django.http import JsonResponse
from .models import Event

def calendar_events_json(request):
    events = Event.objects.filter(end_date__gte=datetime.now())
    event_list = []

    for event in events:
        event_list.append({
            'title': event.name,
            'start': event.start_date.strftime("%Y-%m-%d"),
            'end': event.end_date.strftime("%Y-%m-%d"),
            'description': event.description,
        })

    return JsonResponse(event_list, safe=False)
