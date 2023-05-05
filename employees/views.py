from django.shortcuts import render, redirect
from .models import SoEmployee, SoOut, SoType, Shift
from .forms import SoOutForm, UpdateoOutsForm
from datetime import date, datetime, time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import DateRangeForm 
from django.db.models import Q







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






 


@login_required(login_url='login')
def home(request):
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
    if employee_name is not None and employee_type is not None:
        print(employee_name)
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_em_id_key__em_name__exact=employee_name) & Q(co_fk_type_id_key__description__exact=employee_type)) 
        print(f"results with employee name {employee_name} and Type {employee_type} found {sout.count()} results")
        
    elif employee_name is not None: 
        #sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]))
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date]) & Q(co_fk_em_id_key__em_name__exact=employee_name)) 
        print(f"results with employee name {employee_name}  found {sout.count()} results")
    else:
        sout = SoOut.objects.filter(co_date__range=[start_date, end_date])
        print(f"results with ranges {start_date} to {end_date} found {sout.count()} results")
    
    #sout = SoOut.objects.filter(co_date=str(today))
    sout.order_by('-co_date')

    emp = SoEmployee.objects.all()
    shift = Shift.objects.all()
    for x in shift:
        y_start = x.yellow_start
        r_start = x.red_start

    form = SoOutForm(request.POST or None, initial={'co_time_arrived': datetime.now().time(), 'co_date': date.today()}) 
    if request.method == 'POST':
        employee_name = request.POST.get('co_employee')
        print("employee name: ", employee_name)
        if form.is_valid():
            #form values
            time_arrived = form.instance.co_time_arrived 
            type = form.instance.co_fk_type_id_key.description 
            zone = form.instance.co_fk_em_id_key
           
            print("zone: ", zone)
            if zone == 2:
                time = y_start
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
           
    context = {'sout': sout, 'emp': emp, 'form':form, 'date_today': datetime.today().date(),'date_range_label': date_range_label, 'date_value':str(end_date_datetime), 'type': type}
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
    # if request.user.is_authenticated:
    #     sout = SoOut.objects.get(co_id_key=pk)
    #     sout.delete()
    #     messages.success(request, "deleted successfully")
    # else:
    #     messages.success(request, "You need to be logged in")

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
    sout = SoOut.objects.get(co_id_key=pk)
    form = UpdateoOutsForm(request.POST or None, instance=sout) 
    if request.method == 'POST':
        employee_name = request.POST.get('co_employee')
        print("employee name: ", employee_name)
        if form.is_valid():
            #form values
            time_arrived = request.POST.get('time')
            type = form.instance.co_fk_type_id_key.description 
            zone = form.instance.co_fk_em_id_key
           
            print("zone: ", zone)
            if zone == 2:
                time = y_start
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
                  
                if time_arrived is not None:
                    print("time_arrived:  ",time_arrived)
                    time_arrived_formatted = datetime.strptime(time_arrived, '%H:%M').time()
                    print("time_arrived_formatted:  ",time_arrived_formatted)
                    time_diff = datetime.combine(datetime.today(), time_arrived_formatted ) - datetime.combine(datetime.today(), time) 
                    form.instance.co_time_arrived = time_arrived_formatted
                else:
                    time_diff = None
                form.instance.co_time_dif = str(time_diff)[0:4] 
                form.save() 
                return redirect('home') 
    context = {'form2': form, 'sout': sout}
    return render(request, 'update_co.html', context)

 
  
 

@login_required(login_url='login')
def add_sout_manually(request):
    sout = SoOut.objects.all()
    shift = Shift.objects.all()
    date_value = request.POST.get('date')
    
    for x in shift:
        y_start = x.yellow_start
        r_start = x.red_start 
         
    
    form = UpdateoOutsForm(request.POST or None)
    if request.method == 'POST':

        form.instance.co_time_arrived = request.POST.get('time')
        print("time arrived: ", form.instance.co_time_arrived)
        form.save()
        zone = form.instance.co_fk_em_id_key.em_zone
        if zone == 2:
            time = y_start
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





def logout_user(request):
    logout(request)
    return redirect('login')