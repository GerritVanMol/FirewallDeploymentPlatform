from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
# Create your views here.
from datetime import datetime

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "collega"
    #Convert month name to number
    month = month.title()
    month_number = list(calendar.month_name).index(month)

    cal = HTMLCalendar().formatmonth(
        year, 
        month_number)
    now = datetime.now()
    current_year = now.year


    return render(request,  
    'events/home.html',{
        "some_name": name, 
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        })
