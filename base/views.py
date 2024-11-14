from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone

@login_required
def Dashboard(request):
    user = request.user

    if user.user_type == "farmer":
        context = {
            "user": user
        }
        return render(request, 'base/farmer/dashboard.html', context)
    else:
        all_activities = {}
        all_line_activities = LineActivity.objects.filter(user=user)
        
        for line_activity in all_line_activities:
            if line_activity.end_time:
                time_difference = line_activity.end_time - line_activity.start_time
                total_minutes = int(time_difference.total_seconds() // 60)
                hours, minutes = divmod(total_minutes, 60)
                duration = f"{hours}h {minutes}m"
                line_activity.duration = duration
            else:
                line_activity.duration = "בתהליך"

            field_activity = line_activity.field_activity
            date = field_activity.start_time.strftime('%d/%m/%Y')
            
            if field_activity not in all_activities:
                all_activities[field_activity] = {
                    "date": date,
                    "line_activities": []
                }
            
            all_activities[field_activity]["line_activities"].append(line_activity)
        
        context = {
            "user": user,
            "all_activities": all_activities.values() 
        }

        return render(request, 'base/worker/dashboard.html', context)

@login_required
def Fields_Track(request):
    user = request.user

    if user.user_type != "farmer":
        return redirect('base:dashboard')
    
    all_fields = Field.objects.filter(farmer__user_id = user.user_id)
    for index, field in enumerate(all_fields):
        field.number = index + 1 
    
    context = {
        "user": user,
        "all_fields": all_fields
    }
    
    return render(request, 'base/farmer/fields_track.html', context)

@login_required
def Lines_Track(request, field_id):
    user = request.user

    if user.user_type != "farmer":
        return redirect('base:dashboard')
    
    field = Field.objects.filter(field_id=field_id).first()

    if field.farmer != user:
        return redirect('base:dashboard')

    field_lines = Line.objects.filter(field=field)
    
    context = {
        "user": user,
        "field": field,
        "field_lines": field_lines
    }
    
    return render(request, 'base/farmer/lines_track.html', context)

@login_required
def QR_Define_Field(request):
    user = request.user

    if user.user_type != "farmer":
        return redirect('base:dashboard')

    all_fields = Field.objects.filter(farmer__user_id = user.user_id)
    for index, field in enumerate(all_fields):
        field.number = index + 1 
    
    context = {
        "user": user,
        "all_fields": all_fields
    }

    return render(request, 'base/farmer/qr_define_field.html', context)

@login_required
def QR_Define_Lines(request, field_id):
    user = request.user

    if user.user_type != "farmer":
        return redirect('base:dashboard')
    
    field = Field.objects.filter(field_id=field_id).first()

    if field.farmer != user:
        return redirect('base:dashboard')

    field_lines = Line.objects.filter(field=field)

    if request.method == 'POST':
        checked_lines = request.POST.getlist('checked_lines')
        selected_lines = Line.objects.filter(id__in=checked_lines)

        print([line.line_number for line in selected_lines])
        
        return redirect('base:dashboard')
    
    context = {
        "user": user,
        "field": field,
        "field_lines": field_lines
    }

    return render(request, 'base/farmer/qr_define_lines.html', context)

@login_required
def Choose_Activity_Field(request):
    user = request.user

    if user.user_type != "farmer":
        return redirect('base:dashboard')
    
    all_fields = Field.objects.filter(farmer__user_id = user.user_id)
    for index, field in enumerate(all_fields):
        field.number = index + 1 
    
    context = {
        "user": user,
        "all_fields": all_fields
    }
    
    return render(request, 'base/farmer/choose_activity_field.html', context)

@login_required
def Activity(request, field_id):
    user = request.user

    if user.user_type != "farmer":
        context = {"user": user}

        return render(request, 'base/worker/activity.html', context)

    
    field = Field.objects.filter(field_id=field_id).first()

    if field.farmer != user:
        return redirect('base:dashboard')
    
    field_lines = Line.objects.filter(field=field)
    activity, created = FieldActivity.objects.get_or_create(
        field=field,
        end_time=None,
    )

    if request.method == 'POST':
        action = request.POST.get('start') or request.POST.get('finish')
        if action == 'start':
            # Start the activity
            if activity.start_time is None:
                activity.start_time = timezone.now()
                activity.save()
            # Redirect back to the activity page to show status
            return redirect('base:activity', field_id=field_id)
        elif action == 'finish':
            # End the activity
            if activity.end_time is None:
                activity.end_time = timezone.now()
                activity.save()
            # Redirect to the dashboard after finishing
            return redirect('base:dashboard')

    field_lines_status = []
    for line in field_lines:
        existing_line_activity = LineActivity.objects.filter(line=line, field_activity=activity).first()
        if existing_line_activity:
            if existing_line_activity.end_time:
                status = "נקטף"
                status_class = "done"
            else:
                status = "בתהליך"
                status_class = "in-progress"
        else:
            status = "מחכה"
            status_class = "waiting"
        
        field_lines_status.append({
            "line": line,
            "status": status,
            "status_class": status_class
        })
    
    context = {
        "user": user,
        "activity": activity,
        "field_lines_status": field_lines_status
    }
    
    return render(request, 'base/farmer/activity.html', context)

@login_required
def CreateLineActivity(request, field_id, line_number):
    user = request.user
    
    field = Field.objects.filter(field_id=field_id).first()
    field_activity = FieldActivity.objects.filter(field=field, end_date=None).first()

    if field_activity:
        line = get_object_or_404(Line, field=field, line_number=line_number)
        
        line_activity = LineActivity.objects.create(
            user=user,
            line=line,
            field_activity=field_activity,
            start_time=timezone.now()
        )
        line_activity.save()

    return redirect('base:dashboard')