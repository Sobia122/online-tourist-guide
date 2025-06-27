from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from destinations.models import Destination, Review
from activities.models import Activity
from events.models import Event
from gallery.models import Photo, PhotoInteraction
from geopy.distance import geodesic

@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    interaction, created = PhotoInteraction.objects.get_or_create(
        user=request.user, photo=photo
    )
    interaction.liked = not interaction.liked
    interaction.save()

    like_count = PhotoInteraction.objects.filter(photo=photo, liked=True).count()
    return JsonResponse({'liked': interaction.liked, 'like_count': like_count})

def destination_detail(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    current_date = date.today()

    # Activities and events
    activities = Activity.objects.filter(destination=destination)
    events = Event.objects.filter(destination=destination, start_date__gte=current_date)
    photos = Photo.objects.filter(destination=destination)
    reviews = destination.reviews.all()

    # ✅ Distance calculation (from Islamabad for now)
    try:
        user_location = (33.6844, 73.0479)  # Example: Islamabad coordinates
        destination_location = (destination.latitude, destination.longitude)
        distance_km = round(geodesic(user_location, destination_location).km, 2)
    except:
        distance_km = None

    # ✅ Handle review submission
    if request.method == 'POST' and request.POST.get('submit_review') == '1':
        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            if rating and comment:
                Review.objects.create(
                    destination=destination,
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
                return redirect('destinations:destination_detail', destination_id=destination.id)

    # ✅ Prepare like info for gallery photos
    user_likes = {}
    if request.user.is_authenticated:
        for photo in photos:
            user_likes[photo.id] = PhotoInteraction.objects.filter(
                photo=photo, user=request.user, liked=True
            ).exists()

    return render(request, 'destinations/detail.html', {
        'destination': destination,
        'activities': activities,
        'events': events,
        'photos': photos,
        'user_likes': user_likes,
        'reviews': reviews,
        'average_rating': destination.average_rating(),
        'distance_km': distance_km,
    })
