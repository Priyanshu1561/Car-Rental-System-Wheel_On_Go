import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Car, Order, Contact

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('register')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.name = name
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect('signin')

    return render(request, 'register.html')

def signin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            return redirect('vehicles')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('home')

def vehicles(request):
    cars = Car.objects.all()
    params = {'car': cars}
    return render(request, 'vehicles.html', params)

def bill(request):
    cars = Car.objects.all()
    params = {'cars': cars}
    return render(request, 'bill.html', params)

def order(request):
    if request.method == "POST":
        # Extracting booking details from the form
        billname = request.POST.get('billname', '')
        billemail = request.POST.get('billemail', '')
        billphone = request.POST.get('billphone', '')
        billaddress = request.POST.get('billaddress', '')
        billcity = request.POST.get('billcity', '')
        cars11 = request.POST.get('cars11', '')
        car_color = request.POST.get('car_color', '')
        dayss = int(request.POST.get('dayss', 0))
        pickup_date = request.POST.get('pickup_date', '')
        from_location = request.POST.get('fl', '')
        to_location = request.POST.get('tl', '')

        # Server-side validation
        if not all([billname, billemail, billphone, billaddress, billcity, cars11, car_color, dayss, pickup_date, from_location, to_location]):
            messages.error(request, "Please fill all required fields.")
            return redirect('bill')

        # Price calculation on server side
        prices = {
            'Renault': 2000,
            'Alto 800': 700,
            'Innova Crysta': 3500,
            'Chevy Traverse': 3000,
            'BMW X5': 10000,
            'Honda City': 2500,
            'Mercedes Benz': 40000,
            'Swift Dezire': 1000,
            'KIA': 800,
        }
        rent_per_day = prices.get(cars11, 0)
        total_rent = rent_per_day * dayss

        # Save order to the database
        order = Order(
            name=billname,
            email=billemail,
            phone=billphone,
            address=billaddress,
            city=billcity,
            cars=cars11,
            car_color=car_color,
            days_for_rent=dayss,
            date=pickup_date,
            loc_from=from_location,
            loc_to=to_location
        )
        order.save()

        # Save booking details to session
        request.session['customer_name'] = billname
        request.session['email'] = billemail
        request.session['phone'] = billphone
        request.session['car_choice'] = cars11
        request.session['car_color'] = car_color
        request.session['from_location'] = from_location
        request.session['to_location'] = to_location
        request.session['pickup_date'] = pickup_date
        request.session['days'] = dayss
        request.session['total_rent'] = total_rent

        # Debugging: Print session data to confirm it's being stored
        print("Session data:", request.session.items())  # Check session data

        # Redirect to receipt view
        context = {
            'total_rent': total_rent,
            'car_choice': cars11,
            'car_color': car_color,
            'days': dayss,
            'customer_name': billname,
            'email': billemail,
            'phone': billphone,
            'from_location': from_location,
            'to_location': to_location,
            'pickup_date': pickup_date,
        }
        return render(request, 'receipt.html', context)

    return render(request, 'bill.html')


def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname', '')
        contactemail = request.POST.get('contactemail', '')
        contactnumber = request.POST.get('contactnumber', '')
        contactmsg = request.POST.get('contactmsg', '')

        contact = Contact(name=contactname, email=contactemail, phone_number=contactnumber, message=contactmsg)
        contact.save()
        messages.success(request, "Your message has been sent successfully!")

    return render(request, 'contact.html')

def booking_details(request):
    return render(request, 'bill.html')

# Razorpay Initiate Payment View
def initiate_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get data from the request body
            total_rent = int(data.get('total_rent')) * 100  # Convert INR to paise

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Create Razorpay Order
            payment = client.order.create({
                'amount': total_rent,  # Amount in paise
                'currency': 'INR',
                'payment_capture': '1',  # Auto-capture payment
            })

            return JsonResponse({
                'order_id': payment['id'],
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'amount': total_rent,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Razorpay Payment Callback View
@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
def thank_you(request):
    # Retrieve booking details from the session
    customer_name = request.session.get('customer_name', 'Guest')
    email = request.session.get('email', 'N/A')
    phone = request.session.get('phone', 'N/A')
    car_choice = request.session.get('car_choice', 'N/A')
    car_color = request.session.get('car_color', 'N/A')
    from_location = request.session.get('from_location', 'N/A')
    to_location = request.session.get('to_location', 'N/A')
    pickup_date = request.session.get('pickup_date', 'N/A')
    days = request.session.get('days', 0)
    total_rent = request.session.get('total_rent', 0)

    # Pass data to the template
    context = {
        'customer_name': customer_name,
        'email': email,
        'phone': phone,
        'car_choice': car_choice,
        'car_color': car_color,
        'from_location': from_location,
        'to_location': to_location,
        'pickup_date': pickup_date,
        'days': days,
        'total_rent': total_rent,
    }

    return render(request, 'thank_you.html', context)


