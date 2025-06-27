from django.shortcuts import render, get_object_or_404, redirect
from .models import TravelTip
from .forms import TravelTipForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def submit_tip(request):
    if request.method == "POST":
        form = TravelTipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.user = request.user
            tip.save()
            return JsonResponse({"status": "success"})  # Send success response
    return JsonResponse({"status": "error"})  # Send error response

def tip_list(request):
    tips = TravelTip.objects.all()
    return render(request, 'tips/tip_list.html', {'tips': tips})

def tip_detail(request, pk):
    tip = get_object_or_404(TravelTip, pk=pk)
    return render(request, 'tips/tip_detail.html', {'tip': tip})

def tip_create(request):
    if request.method == 'POST':
        form = TravelTipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tip_list')
    else:
        form = TravelTipForm()
    return render(request, 'tips/tip_form.html', {'form': form})

def tip_update(request, pk):
    tip = get_object_or_404(TravelTip, pk=pk)
    if request.method == 'POST':
        form = TravelTipForm(request.POST, instance=tip)
        if form.is_valid():
            form.save()
            return redirect('tip_list')
    else:
        form = TravelTipForm(instance=tip)
    return render(request, 'tips/tip_form.html', {'form': form})

def tip_delete(request, pk):
    tip = get_object_or_404(TravelTip, pk=pk)
    if request.method == 'POST':
        tip.delete()
        return redirect('tip_list')
    return render(request, 'tips/tip_confirm_delete.html', {'tip': tip})
