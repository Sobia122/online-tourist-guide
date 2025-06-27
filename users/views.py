from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from gallery.models import Photo, PhotoInteraction
from gallery.forms import PhotoForm, CommentForm
from django.db.models import Count, Q
from tours.forms import SavedTripForm
from tours.models import Destination, SavedTrip
from django.db.models import Avg
from bookings.forms import TourBookingForm
from bookings.models import TourBooking
from datetime import timedelta
from django.db.models import Avg, Prefetch
from reviews.models import Review  # if review is in a separate app

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserForm
from activities.models import Activity
from tips.models import TravelTip
from events.models import Event
from users.models import Notification
from destinations.models import Destination
from django.shortcuts import render
from django.db.models import Count
from bookings.models import TourBooking
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model

User = get_user_model()

def calendar_events(request):
    events = Event.objects.all()

    event_list = []
    for event in events:
        event_list.append({
            'title': event.name,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'description': event.description,
        })

    return JsonResponse(event_list, safe=False)


def user_dashboard(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unseen_count = notifications.filter(seen=False).count()

    return render(request, 'user_dashboard.html', {
        'notifications': notifications,
        'unseen_count': unseen_count
    })

def get_current_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

    
def user_login(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(mobile_number=mobile_number)
        except CustomUser.DoesNotExist:
            user_obj = None

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')

        messages.error(request, "Please enter a correct mobile number and password.")
        return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
@login_required
def dashboard(request):
    user = request.user
    tour_form = TourBookingForm()
    photo_form = PhotoForm()
    saved_trip_form = SavedTripForm()

    if request.method == 'POST':
        if 'upload_photo' in request.POST:
            photo_form = PhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.uploaded_by = user
                photo.save()
                messages.success(request, "Photo uploaded successfully.")
                return redirect('users:dashboard')

        elif 'book_tour' in request.POST:
            tour_form = TourBookingForm(request.POST)
            if tour_form.is_valid():
                booking = tour_form.save(commit=False)
                booking.user = user
                booking.save()
                messages.success(request, "Tour booked successfully.")
                return redirect('users:dashboard')

        elif 'save_trip' in request.POST:
            saved_trip_form = SavedTripForm(request.POST)
            if saved_trip_form.is_valid():
                saved_trip = saved_trip_form.save(commit=False)
                saved_trip.user = user
                saved_trip.save()
                messages.success(request, "Trip saved successfully.")
                return redirect('users:dashboard')

        elif 'like_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            photo = get_object_or_404(Photo, id=photo_id)
            interaction, created = PhotoInteraction.objects.get_or_create(user=user, photo=photo)
            interaction.liked = not interaction.liked
            interaction.save()
            return redirect('users:dashboard')

        elif 'comment_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            comment_text = request.POST.get('comment', '').strip()
            if comment_text:
                photo = get_object_or_404(Photo, id=photo_id)
                interaction, created = PhotoInteraction.objects.get_or_create(user=user, photo=photo)
                interaction.comment = comment_text
                interaction.save()
            return redirect('users:dashboard')

        elif 'delete_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            photo = get_object_or_404(Photo, id=photo_id)
            if photo.uploaded_by == user:
                photo.delete()
                messages.success(request, "Photo deleted successfully.")
            else:
                messages.error(request, "You are not authorized to delete this photo.")
            return redirect('users:dashboard')

    # === User Preferences ===
    user_season = user.preferred_season.strip().capitalize() if getattr(user, 'preferred_season', None) else "Summer"
    user_travel_type = user.preferred_travel_type.strip().capitalize() if getattr(user, 'preferred_travel_type', None) else None

    # === Recommended Activities ===
    recommended_activities = Activity.objects.filter(season__iexact=user_season)
    if user_travel_type:
        recommended_activities = recommended_activities.filter(activity_type__iexact=user_travel_type)
    if not recommended_activities.exists():
        recommended_activities = Activity.objects.filter(season__iexact=user_season)
    if not recommended_activities.exists():
        recommended_activities = Activity.objects.all()

    

    # === Recommended Events ===
    recommended_events = Event.objects.filter(destination__season__iexact=user_season).order_by("start_date")
    if not recommended_events.exists():
        recommended_events = Event.objects.filter(end_date__gte=datetime.now()).order_by("start_date")

    # === Travel Tips ===
    travel_tips = {
        user_season: TravelTip.objects.filter(season__iexact=user_season, approved=True)
    }
    default_tips = []
    if not travel_tips[user_season].exists():
        default_tips = [
            {"title": "Pack Light", "content": "Choose versatile clothes."},
            {"title": "Stay Hydrated", "content": "Carry a reusable water bottle."},
            {"title": "Stay Safe", "content": "Follow local safety rules."}
        ]

    # === Recommended Destinations ===
    saved_seasons = SavedTrip.objects.filter(user=user).values_list('destination__season', flat=True)
    recommended_destinations = Destination.objects.filter(season__in=saved_seasons)
    if not recommended_destinations.exists():
        if user_season and user_travel_type:
            recommended_destinations = Destination.objects.filter(season__iexact=user_season, travel_type__iexact=user_travel_type)
        elif user_season:
            recommended_destinations = Destination.objects.filter(season__iexact=user_season)
        elif user_travel_type:
            recommended_destinations = Destination.objects.filter(travel_type__iexact=user_travel_type)
        else:
            recommended_destinations = Destination.objects.all()[:6]

    # === Seasonal Destinations (Popular by Season) ===
    seasonal_destinations = Destination.objects.filter(season__iexact=user_season)

    # === Tab Filter Support ===
    selected_seasons = list(set(season.lower() for season in saved_seasons))

    # === Bookings & Saved Trips ===
    bookings = TourBooking.objects.filter(user=user)
    saved_trips = SavedTrip.objects.filter(user=user)

    # === Photos & Interactions ===
    photos = Photo.objects.all().select_related('uploaded_by').prefetch_related('interactions')
    for photo in photos:
        photo.like_count = photo.interactions.filter(liked=True).count()
        photo.comments = photo.interactions.exclude(comment='').exclude(comment__isnull=True)

    my_photo_count = photos.filter(uploaded_by=user).count()
    my_photo_likes = sum(p.interactions.filter(liked=True).count() for p in photos if p.uploaded_by == user)
    my_photo_comments = sum(p.interactions.exclude(comment='').exclude(comment__isnull=True).count() for p in photos if p.uploaded_by == user)

    # === Notifications ===
    six_months_ago = datetime.now() - timedelta(days=180)
    notifications = Notification.objects.filter(user=user, created_at__gte=six_months_ago).order_by('-created_at')
    unseen_count = notifications.filter(seen=False).count()

    # === Profile Picture ===
    profile_pic_url = user.profile_picture.url if getattr(user, 'profile_picture', None) else "/static/default.png"

    # === Final Context ===
    context = {
        'profile_picture': profile_pic_url,
        'user_preferences': user_travel_type,
        'recommended_activities': recommended_activities,
        'recommended_events': recommended_events,
        'recommended_destinations': recommended_destinations,
        'seasonal_destinations': seasonal_destinations,  # ⬅️ added
        'selected_season': user_season,                  # ⬅️ added
        'travel_tips': travel_tips,
        'default_tips': default_tips,
        'autumn_destinations': Destination.objects.filter(season='Autumn'),
        'spring_destinations': Destination.objects.filter(season='Spring'),
        'summer_destinations': Destination.objects.filter(season='Summer'),
        'winter_destinations': Destination.objects.filter(season='Winter'),
        'selected_seasons': selected_seasons,
        'destination_with_photos': Destination.objects.prefetch_related('gallery_photos').all(),
        'form': tour_form,
        'photo_form': photo_form,
        'saved_trip_form': saved_trip_form,
        'bookings': bookings,
        'saved_trips': saved_trips,
        'notifications': notifications,
        'unseen_count': unseen_count,
        'photos': photos,
        'my_booking_count': bookings.count(),
        'my_saved_trip_count': saved_trips.count(),
        'my_photo_count': my_photo_count,
        'my_photo_likes': my_photo_likes,
        'my_photo_comments': my_photo_comments,
    }

    return render(request, 'users/dashboard.html', context)
@login_required 
def delete_trip(request, trip_id):
    trip = get_object_or_404(SavedTrip, id=trip_id, user=request.user)
    if request.method == "POST":
        trip.delete()
    return redirect('users:dashboard')  
@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    unseen_count = notifications.filter(seen=False).count()  # Count unseen notifications
    return render(request, 'users/notifications.html', {'notifications': notifications, 'unseen_count': unseen_count})

@csrf_exempt
@login_required
def mark_notification_as_read(request, notification_id):
    if request.method == "POST":
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.seen = True
            notification.save()

            unseen_count = request.user.notifications.filter(seen=False).count()  # Updated unseen count
            return JsonResponse({"status": "ok", "unseen_count": unseen_count})
        except Notification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Notification not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def send_booking_notification(user, booking_details):
    message = f"Your booking for {booking_details['destination']} has been confirmed."
    Notification.objects.create(user=user, message=message)

def send_activity_notification(user, activity):
    message = f"New activity '{activity.name}' is available for your travel."
    Notification.objects.create(user=user, message=message)

def send_event_notification(user, event):
    message = f"New event '{event.name}' is happening soon!"
    Notification.objects.create(user=user, message=message)

def send_tip_notification(user, tip):
    message = f"New tip: {tip.title} - {tip.description}"
    Notification.objects.create(user=user, message=message)



@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})


def homepage(request):
    all_destinations = Destination.objects.filter(featured_on_homepage=True)
    
    autumn_destinations = all_destinations.filter(season='Autumn')
    spring_destinations = all_destinations.filter(season='Spring')
    summer_destinations = all_destinations.filter(season='Summer')
    winter_destinations = all_destinations.filter(season='Winter')

    # No annotate, just slice manually
    top_rated_destinations = sorted(
        all_destinations,
        key=lambda d: d.average_rating(),
        reverse=True
    )[:6]

    context = {
        'all_destinations': all_destinations,
        'autumn_destinations': autumn_destinations,
        'spring_destinations': spring_destinations,
        'summer_destinations': summer_destinations,
        'winter_destinations': winter_destinations,
        'top_rated_destinations': top_rated_destinations,
    }

    return render(request, 'users/homepage.html', context)


def analytics_dashboard(request):
    user = request.user

    # === Basic Stats Cards ===
    total_destinations = Destination.objects.count()
    total_bookings = TourBooking.objects.count()
    total_users = User.objects.count()
    total_reviews = Destination.objects.annotate(review_count=Count('reviews')).aggregate(total=Count('review_count'))['total'] or 0

    stats_cards = [
        {'label': 'Destinations', 'value': total_destinations, 'color': '#3498db'},
        {'label': 'Bookings', 'value': total_bookings, 'color': '#2ecc71'},
        {'label': 'Users', 'value': total_users, 'color': '#f1c40f'},
        {'label': 'Reviews', 'value': total_reviews, 'color': '#e67e22'},
    ]

    # === Seasonal Bookings ===
    season_counts = TourBooking.objects.values('category').annotate(count=Count('id'))
    season_data = {'winter': 0, 'summer': 0, 'autumn': 0}
    season_map = {1: 'winter', 2: 'summer', 3: 'autumn'}

    for item in season_counts:
        season = season_map.get(item['category'], '').lower()
        if season in season_data:
            season_data[season] = item['count']

    # === Rating Distribution ===
    destinations = Destination.objects.annotate(avg_rating=Avg('reviews__rating'))
    high = destinations.filter(avg_rating__gte=4).count()
    medium = destinations.filter(avg_rating__gte=2, avg_rating__lt=4).count()
    low = destinations.filter(avg_rating__lt=2).count()
    rating_data = {'high': high, 'medium': medium, 'low': low}

    # === Top Rated ===
    top_rated = destinations.order_by('-avg_rating')[:5]

    # === Most Visited ===
    most_visited_raw = TourBooking.objects.values('destination__name').annotate(count=Count('id')).order_by('-count')[:5]
    most_visited = []
    for item in most_visited_raw:
        try:
            dest = Destination.objects.get(name=item['destination__name'])
            most_visited.append((dest, item['count']))
        except Destination.DoesNotExist:
            continue

    # === Favorite Destinations ===
    favorite_dest_raw = TourBooking.objects.filter(user=user).values('destination__name').annotate(count=Count('id')).order_by('-count')[:5]
    favorite_destinations = []
    for item in favorite_dest_raw:
        try:
            dest = Destination.objects.get(name=item['destination__name'])
            favorite_destinations.append({'name': dest.name, 'visit_count': item['count']})
        except Destination.DoesNotExist:
            continue

    # ✅ Personalized Recommendations from SavedTrip
    saved_trips = SavedTrip.objects.filter(user=user).select_related('destination')
    personalized_recommendations = [
        f"{trip.destination.name} — based on your saved trip" for trip in saved_trips if trip.destination
    ]

    return render(request, 'users/analytics_dashboard.html', {
        'stats_cards': stats_cards,
        'season_data': season_data,
        'rating_data': rating_data,
        'top_rated': top_rated,
        'most_visited': most_visited,
        'favorite_destinations': favorite_destinations,
        'personalized_recommendations': personalized_recommendations,
    })
def custom_logout(request):
    logout(request)
    return redirect('homepage')
