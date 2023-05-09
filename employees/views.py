from django.shortcuts import render, redirect
from .models import SoEmployee, SoOut, SoType, Shift
from .forms import SoOutForm, UpdateoOutsForm
from datetime import date, datetime, time, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import DateRangeForm 
from django.db.models import Q
from django.http import HttpResponse


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
    print("check: ", check)
    if employee_name is not None and employee_type is not None:
        print(employee_name)
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_em_id_key__em_name__exact=employee_name) & Q(co_fk_type_id_key__description__exact=employee_type)) 
        print(f"results with employee name {employee_name} and Type {employee_type} found {sout.count()} results")
        
    elif employee_name is not None and check is None:
        print("check: ", check) 
        #sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]))
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_em_id_key__em_name__exact=employee_name)) 
        date_range_label = f"Transactions for {employee_name} for {today.strftime('%B %d, %Y')} | found {sout.count()} results"
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
        date_range_label = f"Showing all Transactions"
        sout = SoOut.objects.all()
    else:
        sout = SoOut.objects.filter(co_date__range=[start_date, end_date])
        date_range_label = f"Transactions for {start_date} | found {sout.count()} results"
    
    #sout = SoOut.objects.filter(co_date=str(today))
    sout.order_by('-co_date')
    
    time_diff_total = timedelta()
    print("time diff total: ", time_diff_total) 
    emp = SoEmployee.objects.all()
    emp.order_by('-em_name')
    shift = Shift.objects.all()
    for x in shift:
        y_start = x.yellow_start
        r_start = x.red_start
        g_start = x.green_start

    # print("y_start", y_start)
    # print("red_start", r_start)
    # print("green_start", g_start)
 
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
            #form values
            time_arrived = form.instance.co_time_arrived 
            type = form.instance.co_fk_type_id_key.description 
            zone = form.instance.co_fk_em_id_key.em_zone
           
            print("zone: ", zone)
            if zone == 2:
                time = y_start
            elif zone == 3:
                time = g_start
            else:
                time = r_start
 

            #get employee name from form and assign it to the instance
            employee_name = request.POST.get('co_employee') 
            form.instance.co_fk_em_id_key.em_name = employee_name

            #check type of absence
            if type == "Vacation" or type == "Call-out" or type == "Left early":
                form.instance.co_time_arrived = None
                form.instance.co_time_dif = None 
                form.save()
                messages.success(request, f"Marked as {type}")
                return redirect('home') 
            else:  
                form.save()  
                if form.instance.co_time_arrived is not None:
                    time_diff = datetime.combine(datetime.today(), time_arrived ) - datetime.combine(datetime.today(), time) 
                else:
                    time_diff = None
                form.instance.co_time_dif = str(time_diff)[0:4] 
                 
                form.save() 
                
                return redirect('home') 
         
    context = {'sout': sout, 'emp': emp, 'form':form, 'date_today': datetime.today().date(),'date_range_label': date_range_label, 'date_value':str(end_date_datetime), 'type': type,'total_time_diff': total_time_diff_formatted}
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

            if zone == 2:
                time = y_start
            elif zone == 3:
                time = g_start
            else:
                time = r_start

            # get employee name from form and assign it to the instance
            employee_name = request.POST.get('co_employee')
            form.instance.co_fk_em_id_key.em_name = employee_name

            # check type of absence
            if type == "Vacation" or type == "Call-out" or type == "Left early":
                form.instance.co_time_arrived = None
                form.instance.co_time_dif = None
                form.save()
                messages.success(request, f"Marked as {type}")
                return redirect('home')
            else:
                if time_arrived is not None:
                    print("time_arrived:  ", time_arrived)
                    form.instance.co_time_arrived = time_arrived
                    time_diff = datetime.combine(datetime.today(), time_arrived) - datetime.combine(
                        datetime.today(), time)
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

        form.instance.co_time_arrived = request.POST.get('time')
        print("time arrived: ", form.instance.co_time_arrived)
        form.save()
        zone = form.instance.co_fk_em_id_key.em_zone
        print("zone: ", zone)
        if zone == 2:
            time = y_start
        elif zone == 3:
            time = g_start
        else:
            time = r_start  


        time_value = request.POST.get('time')
        if time_value == "":
            time_obj = None
        else:
            time_obj = datetime.strptime(time_value, '%H:%M').time()
        date_value = request.POST.get('date')
        date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
        print("date obj: ", date_obj)
        form.instance.co_date = date_obj
        form.instance.co_time_arrived = time_obj
            
        form.save()  
        if time_obj is not None:
            time_diff = datetime.combine(datetime.today(), time_obj) - datetime.combine(datetime.today(), time) 
        else:
            time_diff = None
        form.instance.co_time_dif = str(time_diff)[0:4]
        print("time diff: ", form.instance.co_time_dif)
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