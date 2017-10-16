import random
from linecache import cache

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.forms import RegisterationForm
import http.client




@login_required
def home(request):
    return render(request, 'home.html')


def registerationform(request):
    if request.method == 'POST':
        #text = request.POST['text']
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.contact_number = form.cleaned_data.get('contact_number')
            user.profile.iam_name = form.cleaned_data.get('iam_name')
            username = form.cleaned_data.get('username')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterationForm()
    return render(request, 'register.html', {'form': form})

def _get_otp(length=5):
    """ Return a numeric PIN with length digits """
    return random.sample(range(10**(length-1), 10**length), 1)[0]


def _verify_otp(contact_number, otp):
    """ Verify a PIN is correct """
    return otp == cache.get(contact_number)


def ajax_send_otp(request):
    """ Sends SMS OTP to the specified number """
    contact_number = request.POST.get('contact_number', "")
    if not contact_number:
        return HttpResponse("No contact number", mimetype='text/plain', status=403)

    otp = _get_otp()

    # store the PIN in the cache for later verification.
    cache.set(contact_number)# valid for 24 hrs

    conn = http.client.HTTPConnection("2factor.in")
    randomOTP = random.randint(1111, 9999)
    conn.request("GET","https://2factor.in/API/R1/?module=SMS_OTP&apikey=7ef37c63-a1dd-11e7-94da-0200cd936042&to=&otpvalue=AUTOGEN")
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))



class OrderForm(object):
    pass


def process_order(request):
    """ Process orders made via web form and verified by SMS PIN. """
    form = OrderForm(request.POST or None)

    if form.is_valid():
        otp= int(request.POST.get("pin", "0"))
        contact_number = request.POST.get("contact_number", "")

        if _verify_otp(contact_number, otp):
            form.save()
            return redirect('transaction_complete')
        else:
            messages.error(request, "Invalid OTP!")
    else:
        return render(
                    request,
                    'register.html',
                    {
                        'form': form
                    }
                )


