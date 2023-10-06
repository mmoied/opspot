from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from .scraper_tester import *
import json
from django.http import JsonResponse

def get_data(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        # form = CredentialForm(request.POST)
        date_range=request.POST.get('date_range')
        email=request.POST.get('email')
        password=request.POST.get('password')
        # check whether it's valid:
        start_date = date_range.split(' - ')[0]
        end_date = date_range.split(' - ')[1]
        # try:
        df = scrape_website(email,password,start_date,end_date)
        print("moied")
        print(df)
        if type(df) != str :
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=export.csv'  # alter as needed
            df.to_csv(path_or_buf=response)  # with other applicable parameters
            return response
        else:
            if df == "No data available in the date range":
                    return JsonResponse({'msg' : df,'status':'ok'})
            else:
                return JsonResponse({'msg' : df,'status':'error'})


    return render(request, "home.html", {})
# Create your views here.


def contact_us(request):
    # CONTACT FORM
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        form_data = {
            'name': name,
            'email': email,
            'message': message,
        }
        message = '''
        From:\n\t\t{}\n
        Message:\n\t\t{}\n
        Email:\n\t\t{}\n
        '''.format(form_data['name'], form_data['message'], form_data['email'])
        # send_mail('You got a mail!', message, '', ['mmoied44@gmail.com'])  # TODO: enter your email address
        send_mail(
            'You got a mail!',
            message,
            'support@flipae.com',
            ['support@flipae.com']
        )

    return render(request, 'test_form.html', {})