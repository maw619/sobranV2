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
    
    
    result = request.GET.get('employee_name')
    if result is not None:
        print(result)
        sout = SoOut.objects.filter(Q(co_date__range=[start_date, end_date])  and Q(co_fk_em_id_key__em_name__icontains=result))
    else:
        sout = SoOut.objects.filter(co_date__range=[start_date, end_date])
    # sout = SoOut.objects.filter(co_date=str(today))
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
            if zone == 1:
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
           
    context = {'sout': sout, 'emp': emp, 'form':form, 'date_today': datetime.today().date(),'date_range_label': date_range_label, 'date_value':str(end_date_datetime)}
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
    sout = SoOut.objects.get(co_id_key=pk)
    shift = Shift.objects.all()
    date_value = request.POST.get('date')
    date_obj = datetime.strptime(str(sout.co_date), '%Y-%m-%d').date()
    print("time from database", sout.co_time_arrived.strftime('%H:%M'))
    print("date from database", sout.co_date)   
    print("date from object", date_obj)   
    for x in shift:
        y_start = x.yellow_start
        r_start = x.red_start 
         
    form = UpdateoOutsForm(instance=sout) 
    if request.method == 'POST':
        form = UpdateoOutsForm(request.POST, instance=sout)

        print("time arrived: ", form.instance.co_time_arrived)
        form.save()
        zone = form.instance.co_fk_em_id_key.em_zone
        if zone == 1:
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
    context = {'time': form.instance.co_time_arrived, 'name': form.instance.co_fk_em_id_key, 'date': str(sout.co_date) , 'time_value': sout.co_time_arrived.strftime('%H:%M'),'form': form}
    return render(request, 'update_co.html', context)
 








def logout_user(request):
    logout(request)
    return redirect('login')