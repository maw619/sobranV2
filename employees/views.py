from django.shortcuts import render, redirect
from .models import SoEmployee, SoOut, SoType, Shift
from .forms import SoOutForm, UpdateoOutsForm
from datetime import date, datetime, time, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import DateRangeForm 
from django.db.models import Q
from django.http import HttpResponse,HttpResponseBadRequest



def login_user(request):
     
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'login.html')






def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address

 


@login_required(login_url='login')
def home(request):
    print(get_client_ip(request))
    today = date.today()
    type = SoType.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    end_date_datetime = ""

    if start_date is None or end_date is None or start_date is "" or end_date is "":
        date_range_label = f"Transactions for {datetime.today().date().strftime('%B %d, %Y')}"
        start_date = today
        end_date = today
    else: 
        start_date = request.GET.get('start_date')
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        start_date_formatted = start_date_datetime.strftime('%B %d, %Y')  

        end_date = request.GET.get('end_date')
        end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        end_date_formatted = end_date_datetime.strftime('%B %d, %Y')

        date_range_label = f"Transactions for {start_date_formatted} to {end_date_formatted}"
    
    employee_name = request.GET.get('employee_name')
    employee_type = request.GET.get('employee_type')
    check = request.GET.get('check')
    if employee_name is not None and employee_type is not None:
        print(employee_name)
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_em_id_key__em_name__exact=employee_name) & Q(co_fk_type_id_key__description__exact=employee_type)) 
        print(f"results with employee name {employee_name} and Type {employee_type} found {sout.count()} results")
        
    elif employee_name is not None and check is None:
        print("check: ", check) 
        #sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]))
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_em_id_key__em_name__exact=employee_name)) 
        date_range_label = f"Transactions for {employee_name} for {today} | found {sout.count()} results"
        print(f"results with employee name {employee_name} | found {sout.count()} results")
    elif employee_name is not None and check == "on":
        print("check: ", check)
        sout = SoOut.objects.filter(Q(co_fk_em_id_key__em_name__exact=employee_name) & Q(co_date__isnull=False))
        date_range_label = f"All Transactions for {employee_name} | found {sout.count()} results"
        print(f"results with employee name {employee_name}  found {sout.count()} results")
    elif employee_name is None and employee_type is not None and check == "on":
        print("check: ", check)
        sout = SoOut.objects.filter(Q(co_fk_type_id_key__description__exact=employee_type) & Q(co_date__isnull=False))
        date_range_label = f"Transactions for {employee_type} | found {sout.count()} results"
    elif employee_type is not None and employee_name is None:
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_type_id_key__description__exact=employee_type))  
        date_range_label = f"Transactions for {employee_type} for {start_date} to {end_date} | found {sout.count()} results" 
    elif employee_type is not None and employee_name is not None:
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_em_id_key__em_name__exact=employee_name) & Q(co_fk_type_id_key__description__exact=employee_type)) 
        date_range_label = f"Transactions for {employee_name} and Type {employee_type} found {sout.count()} results || and date ranges specified {start_date} to {end_date} | found {sout.count()} results"
    elif employee_name is not None and employee_type is not None:
        sout = SoOut.objects.filter(co_fk_em_id_key__em_name__exact=employee_name, co_fk_type_id_key__description__exact=employee_type)
        date_range_label = f"Transactions for {employee_name} and Type {employee_type} found {sout.count()} results || and date ranges not specified | found {sout.count()} results"
    elif employee_type is not None and employee_name is None and start_date is None and end_date is None:
        sout = SoOut.objects.filter(co_fk_type_id_key__description__exact=employee_type)
        date_range_label = f"Transactions for Type ({employee_type}) found {sout.count()} results || and date ranges and employee_name not specified either | found {sout.count()} results"
    elif employee_name is not None and check == "on":
        print("check: ", check)
        sout = SoOut.objects.filter(Q(co_fk_em_id_key__em_name__exact=employee_name) & Q(co_date__isnull=True))
        date_range_label = f"Transactions for {employee_name} for {start_date} | found {sout.count()} results"
    elif start_date is today and end_date is today and check == "on":
        sout = SoOut.objects.all()
        date_range_label = f"Showing all Transactions | found {sout.count()} results"
    elif start_date != end_date is not None and employee_name is None and employee_type is None and check is None:
        print("inside start date and end date")
        sout = SoOut.objects.filter(co_date__range=[start_date, end_date])
        date_range_label = f"Transactions for {start_date} to {end_date} | found {sout.count()} results"
    
    #  this doesnt work
    # elif start_date == end_date and employee_name is None and employee_type is None and check is None: 
    #     sout = SoOut.objects.filter(co_date=start_date)
    #     date_range_label = f"Transactions for {start_date} | found {sout.count()} results"
    else:  
        sout = SoOut.objects.filter(co_date=start_date)
        date_range_label = f"Transactions for {start_date} | found {sout.count()} results"
    
    #sout = SoOut.objects.filter(co_date=str(today))
    sout.order_by('-co_date')
    
    time_diff_total = timedelta() 
    emp = SoEmployee.objects.all()
    emp.order_by('-em_name')
    shift = Shift.objects.all() 
     
             

    time_diff_total = timedelta()
    for item in sout:
        if item.co_time_dif is not None and ":" in item.co_time_dif:
            hours, minutes = map(int, item.co_time_dif.split(':'))
            time_diff = timedelta(hours=hours, minutes=minutes)
            time_diff_total += time_diff

    # Calculate the total hours and minutes
    total_minutes = time_diff_total.total_seconds() // 60
    total_hours = total_minutes // 60
    minutes_remaining = total_minutes % 60

    # Format the total time difference as "hh:mm"
    total_time_diff_formatted = f"{int(total_hours):02d}:{int(minutes_remaining):02d}" if time_diff_total else ""
 

    # Convert the total time difference to a formatted string
    total_time_diff_formatted = str(time_diff_total)

    form = SoOutForm(request.POST or None, initial={'co_time_arrived': datetime.now().time(), 'co_date': date.today()})
    if request.method == 'POST':
        employee_name = request.POST.get('co_employee')
        print("employee name: ", employee_name)
        if form.is_valid():
            # Form values
            time_arrived = form.instance.co_time_arrived
            type = form.instance.co_fk_type_id_key.description
            zone = form.instance.co_fk_em_id_key.em_zone

            for x in shift:
                y_start = x.yellow_start
                r_start = x.red_start
                g_start = x.green_start

                y_end = x.yellow_end
                r_end = x.red_end
                g_end = x.green_end

             
            # Get employee name from form and assign it to the instance
            employee_name = request.POST.get('co_employee')
            form.instance.co_fk_em_id_key.em_name = employee_name

            # Check type of absence
            if type == "Vacation" or type == "Call-out":
                if zone == 1: 
                    yellow_shift_start = datetime.combine(datetime.today(), y_start)
                    yellow_shift_end = datetime.combine(datetime.today(), y_end)
                    time_shift = (yellow_shift_end - yellow_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home')
                    
                elif zone == 2:
                    print("here from zone 2")
                    red_shift_start = datetime.combine(datetime.today(), r_start)
                    red_shift_end = datetime.combine(datetime.today(), r_end)
                    time_shift = (red_shift_end - red_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home') 

                else:
                    green_shift_end = datetime.combine(datetime.today(), g_end)
                    green_shift_start = datetime.combine(datetime.today(), g_start)
                    time_shift = (green_shift_end - green_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home')

            elif type == "Left early" and time_arrived is not None:
                if zone == 1: 
                    yellow_shift_end = datetime.combine(datetime.today(), y_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived)
                    print("inside zone 1 and in left early")
                    time_diff = yellow_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_diff: ", time_diff_str)
                    form.instance.co_time_dif = time_diff_str
                    form.save()  
                    return redirect('home') 
                elif zone == 2: 
                    red_shift_end = datetime.combine(datetime.today(), r_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived)
                    print("inside zone 2 and in left early")
                    time_diff = red_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_diff: ", time_diff_str)
                    form.instance.co_time_dif = time_diff_str
                    form.save()  
                    return redirect('home') 
                else: 
                    green_shift_end = datetime.combine(datetime.today(), g_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived)
                    print("inside zone 3 and in left early")
                    time_diff = green_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_diff: ", time_diff_str)
                    form.instance.co_time_dif = time_diff_str
                    form.save()  
                    return redirect('home')
            else:  
                if form.instance.co_time_arrived is not None: 
                    if zone == 1:
                        time_diff = datetime.combine(datetime.today(), datetime.now().time() ) - datetime.combine(datetime.today(), y_start) 
                        print("time_diff: zone 1", time_diff)
                        form.instance.co_time_arrived = datetime.now().time()
                        form.instance.co_time_dif = str(time_diff)[0:4]
                        form.save()  
                        return redirect('home')
                    elif zone == 2:
                        time_diff = datetime.combine(datetime.today(), datetime.now().time() ) - datetime.combine(datetime.today(), r_start)
                        print("time_diff: zone 2", time_diff)
                        form.instance.co_time_arrived = datetime.now().time()
                        form.instance.co_time_dif = str(time_diff)[0:4]
                        form.save()  
                        return redirect('home')
                    else:
                        time_diff = datetime.combine(datetime.today(), datetime.now().time() ) - datetime.combine(datetime.today(), g_start)
                        print("time_diff: zone", time_diff)
                        form.instance.co_time_arrived = datetime.now().time()
                        form.instance.co_time_dif = str(time_diff)[0:4]
                        form.save()  
                        return redirect('home')
                    
                
                    
                 
                 
         
    context = {'sout': sout, 'emp': emp, 'form':form, 'date_today': datetime.today().date(),'date_range_label': date_range_label, 'date_value':str(end_date_datetime), 'type': type,'total_time_diff': total_time_diff_formatted[:4]}
    return render(request, 'home.html', context)




def date_range_view(request):
    form = DateRangeForm()
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date'] 
            print("start date: ", start_date)
            print("end date: ", end_date)
            so_out = SoOut.objects.filter(co_date__range=[start_date, end_date])
            print("so out: ", so_out)
            context = {'so_out': so_out, 'form': form}
            return render(request, 'dates.html', context)
    return render(request, 'dates.html', {'form': form})



 
def delete_so_out(request, pk): 
    sout = SoOut.objects.get(co_id_key=pk)
    sout.delete()
    messages.success(request, "deleted successfully")
    return redirect('home')




def update_so_out(request, pk):
    emp = SoEmployee.objects.all()
    shift = Shift.objects.all()

    for x in shift:
        y_start = x.yellow_start
        r_start = x.red_start
        g_start = x.green_start

        y_end = x.yellow_end
        r_end = x.red_end
        g_end = x.green_end

    sout = SoOut.objects.get(co_id_key=pk)
    print(sout.co_date)
    employee_name = request.POST.get('co_employee')
    form = UpdateoOutsForm(request.POST or None, instance=sout)

    if request.method == 'POST':
        
        print("employee name: ", employee_name)
        if form.is_valid():
            # form values
            time_arrived = form.cleaned_data['co_time_arrived']
            type = form.instance.co_fk_type_id_key.description
            zone = form.instance.co_fk_em_id_key.em_zone
            print(f"zone for {form.instance.co_fk_em_id_key}: ", zone)

            if zone == 1:
                time = y_start
            elif zone == 2:
                time = r_start
            else:
                time = g_start

            # get employee name from form and assign it to the instance
            employee_name = request.POST.get('co_employee')
            form.instance.co_fk_em_id_key.em_name = employee_name

            # check type of absence
            if type == "Vacation" or type == "Call-out":
                if zone == 1: 
                    yellow_shift_start = datetime.combine(datetime.today(), y_start)
                    yellow_shift_end = datetime.combine(datetime.today(), y_end)
                    time_shift = (yellow_shift_end - yellow_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home')
                    
                elif zone == 2:
                    print("here from zone 2")
                    red_shift_start = datetime.combine(datetime.today(), r_start)
                    red_shift_end = datetime.combine(datetime.today(), r_end)
                    time_shift = (red_shift_end - red_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home') 

                else:
                    green_shift_end = datetime.combine(datetime.today(), g_end)
                    green_shift_start = datetime.combine(datetime.today(), g_start)
                    time_shift = (green_shift_end - green_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home')
                 
                   
            elif type == "Left early" and time_arrived is not None:
                if zone == 1: 
                    yellow_shift_end = datetime.combine(datetime.today(), y_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived)
                    print("inside zone 1 and in left early")
                    time_diff = yellow_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_diff: ", time_diff_str)
                    form.instance.co_time_dif = time_diff_str
                    form.save()  
                    return redirect('home') 
                elif zone == 2: 
                    red_shift_end = datetime.combine(datetime.today(), r_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived)
                    print("inside zone 2 and in left early")
                    time_diff = red_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_diff: ", time_diff_str)
                    form.instance.co_time_dif = time_diff_str
                    form.save()  
                    return redirect('home') 
                else: 
                    green_shift_end = datetime.combine(datetime.today(), g_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived)
                    print("inside zone 3 and in left early")
                    time_diff = green_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_diff: ", time_diff_str)
                    form.instance.co_time_dif = time_diff_str
                    form.save()  
                    return redirect('home')
 
            else:
                if time_arrived is not None:
                    print("time_arrived:  ", time_arrived)
                    form.instance.co_time_arrived = time_arrived
                    time_diff = datetime.combine(datetime.today(), time_arrived) - datetime.combine(datetime.today(), time)
                else:
                    time_diff = None
                form.instance.co_time_dif = str(time_diff)[0:4] 
            form.save()
            return redirect('home')

    context = {'form2': form, 'name': form.instance.co_fk_em_id_key.em_name}
    return render(request, 'update_co.html', context)



 
  
 

@login_required(login_url='login')
def add_sout_manually(request):
    sout = SoOut.objects.all()
    shift = Shift.objects.all()
    date_value = request.POST.get('date')
    
    for x in shift:
        y_start = x.yellow_start
        r_start = x.red_start 
        g_start = x.green_start  
    
    form = UpdateoOutsForm(request.POST or None)
    if request.method == 'POST':
        employee_name = request.POST.get('co_employee')
        print("employee name: ", employee_name)
        if form.is_valid():
            # Form values
            time_arrived = form.instance.co_time_arrived
            type = form.instance.co_fk_type_id_key.description
            zone = form.instance.co_fk_em_id_key.em_zone

            for x in shift:
                y_start = x.yellow_start
                r_start = x.red_start
                g_start = x.green_start

                y_end = x.yellow_end
                r_end = x.red_end
                g_end = x.green_end


            # Get employee name from form and assign it to the instance
            employee_name = request.POST.get('co_employee')
            form.instance.co_fk_em_id_key.em_name = employee_name
            form_time = request.POST.get('time')
            # Check type of absence
            if type == "Vacation" or type == "Call-out":
                if zone == 1: 
                    yellow_shift_start = datetime.combine(datetime.today(), y_start)
                    yellow_shift_end = datetime.combine(datetime.today(), y_end)
                    time_shift = (yellow_shift_end - yellow_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home')
                    
                elif zone == 2:
                    print("here from zone 2")
                    red_shift_start = datetime.combine(datetime.today(), r_start)
                    red_shift_end = datetime.combine(datetime.today(), r_end)
                    time_shift = (red_shift_end - red_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home') 

                else:
                    green_shift_end = datetime.combine(datetime.today(), g_end)
                    green_shift_start = datetime.combine(datetime.today(), g_start)
                    time_shift = (green_shift_end - green_shift_start).total_seconds() // 60

                    hours, minutes = divmod(time_shift, 60)
                    formatted_time = '{:02d}:{:02d}'.format(int(hours), int(minutes))

                    # Add 30 minutes to the time
                    time_delta = timedelta(minutes=30)
                    updated_time = datetime.strptime(formatted_time, '%H:%M') - time_delta
                    formatted_updated_time = updated_time.strftime('%H:%M')

                    form.instance.co_time_arrived = None
                    form.instance.co_time_dif = formatted_updated_time

                    form.save()
                    return redirect('home')

            elif type == "Left early" and time_arrived is not None:
                time_arrived_str = request.POST.get('time')
                time_arrived2 = datetime.strptime(time_arrived_str, "%H:%M").time()
                
                if zone == 1:
                    time = y_start
                    yellow_shift_end = datetime.combine(datetime.today(), y_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived2)
                    print("inside zone 1 and in left early")
                    time_diff = yellow_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_arrived_dt: ", time_arrived_dt)
                    form.instance.co_time_arrived = time_arrived_dt
                    form.instance.co_time_dif = time_diff_str
                    form.save()
                    return redirect('home')
                elif zone == 2:
                    time = r_start
                    red_shift_end = datetime.combine(datetime.today(), r_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived2)
                    print("inside zone 2 and in left early")
                    time_diff = red_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_arrived_dt: ", time_arrived_dt)
                    form.instance.co_time_arrived = time_arrived_dt
                    form.instance.co_time_dif = time_diff_str
                    form.save()
                    return redirect('home')
                else:
                    time = g_start
                    green_shift_end = datetime.combine(datetime.today(), g_end)
                    time_arrived_dt = datetime.combine(datetime.today(), time_arrived2)
                    print("inside zone 3 and in left early")
                    time_diff = green_shift_end - time_arrived_dt
                    hours, minutes = divmod(time_diff.seconds // 60, 60)
                    time_diff_str = f"{hours:02d}:{minutes:02d}"
                    print("time_arrived_dt: ", time_arrived_dt)
                    form.instance.co_time_arrived = time_arrived_dt
                    form.instance.co_time_dif = time_diff_str
                    form.save()
                    return redirect('home')
 
            else:
                if form.instance.co_time_arrived is not None:
                    time_arrived_str = request.POST.get('time')
                    time_arrived = datetime.strptime(time_arrived_str, '%H:%M').time()  # Convert string to datetime.time
                    if zone == 1:
                        time_diff = datetime.combine(datetime.today(), time_arrived) - datetime.combine(datetime.today(), y_start)
                        print("time_diff: zone 1", time_diff)
                        form.instance.co_time_arrived = datetime.now().time()
                        form.instance.co_time_dif = str(time_diff)[0:4]
                        form.save()
                        return redirect('home')
                    elif zone == 2:
                        time_diff = datetime.combine(datetime.today(), time_arrived) - datetime.combine(datetime.today(), r_start)
                        print("time_diff: zone 2", time_diff)
                        form.instance.co_time_arrived = datetime.now().time()
                        form.instance.co_time_dif = str(time_diff)[0:4]
                        form.save()
                        return redirect('home')
                    else:
                        time_diff = datetime.combine(datetime.today(), time_arrived) - datetime.combine(datetime.today(), g_start)
                        print("time_diff: zone", time_diff)
                        form.instance.co_time_arrived = datetime.now().time()
                        form.instance.co_time_dif = str(time_diff)[0:4]
                        form.save()
                        return redirect('home')

                    
    context = {'form': form}
    return render(request, 'home.html', context)





def view_transaction(request, pk):
    if request.user.is_authenticated:
        sout = SoOut.objects.get(co_id_key=pk)
        return render(request, 'transaction.html', {'sout':sout})
    messages.success(request, "You need to be logged in")
    return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')