from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Tip
from .forms import TipForm
from datetime import timedelta, datetime, date
import calendar

@login_required
def tip_list(request):
    # Get the date from the request parameters or use today's date
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = now().date()
    else:
        selected_date = now().date()

    print(f"Selected date: {selected_date}")

    # Handle form submission
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            selected_date = datetime.strptime(request.POST.get('selected_date'), '%Y-%m-%d').date()
            print(f"Submitted selected date: {selected_date}")
            tip.user = request.user
            tip.date = selected_date  # Ensure the correct date is assigned
            tip.save()
            return redirect(f'/?date={selected_date}')

    # Get tips for the selected date
    tips = Tip.objects.filter(user=request.user, date=selected_date)
    form = TipForm()

    context = {
        'tips': tips,
        'form': form,
        'selected_date': selected_date,
        'previous_date': selected_date - timedelta(days=1),
        'next_date': selected_date + timedelta(days=1),
    }
    return render(request, 'tips/tip_list.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Tip

@login_required
def tip_stats(request):
    tips = Tip.objects.filter(user=request.user)
    
    total_tips = sum(tip.amount for tip in tips)
    total_hours = sum(tip.hours_worked for tip in tips)
    total_days = tips.values('date').distinct().count()
    
    average_tips_per_hour = total_tips / total_hours if total_hours > 0 else 0
    average_tips_per_day = total_tips / total_days if total_days > 0 else 0
    
    shift_types = ['cart', 'morning', 'afternoon']
    average_tips_per_day_by_shift = {}
    average_tips_per_hour_by_shift = {}
    
    for shift in shift_types:
        shift_tips = tips.filter(shift_type=shift)
        shift_total_tips = sum(tip.amount for tip in shift_tips)
        shift_total_hours = sum(tip.hours_worked for tip in shift_tips)
        shift_total_days = shift_tips.values('date').distinct().count()
        
        average_tips_per_day_by_shift[shift] = shift_total_tips / shift_total_days if shift_total_days > 0 else 0
        average_tips_per_hour_by_shift[shift] = shift_total_tips / shift_total_hours if shift_total_hours > 0 else 0
    
    context = {
        'total_tips': total_tips,
        'average_tips_per_hour': average_tips_per_hour,
        'average_tips_per_day': average_tips_per_day,
        'average_tips_per_day_by_shift': average_tips_per_day_by_shift,
        'average_tips_per_hour_by_shift': average_tips_per_hour_by_shift,
    }
    
    return render(request, 'tips/tip_stats.html', context)


@login_required
def tip_calendar(request):
    today = date.today()
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    year = int(year)
    month = int(month)

    # Get tips for the current month
    tips = Tip.objects.filter(user=request.user, date__year=year, date__month=month)

    # Create a matrix for the calendar
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)
    calendar_data = []

    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                tips_for_day = tips.filter(date__day=day)
                total_tips = sum(tip.amount for tip in tips_for_day)
                week_data.append({
                    'day': day,
                    'total_tips': total_tips
                })
        calendar_data.append(week_data)

    context = {
        'calendar_data': calendar_data,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
    }
    return render(request, 'tips/tip_calendar.html', context)

@login_required
def add_tip(request):
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.user = request.user
            tip.save()
            return redirect('tip_list')
    else:
        form = TipForm()
    return render(request, 'tips/add_tip.html', {'form': form})
