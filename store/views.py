from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import stripe
from .models import Product, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    products = Product.objects.all()
    orders = Order.objects.filter(paid=True)
    return render(request, "store/home.html", {"products": products, "orders": orders})

def create_checkout_session(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product.name},
                "unit_amount": product.price * 100,
            },
            "quantity": quantity,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )

    Order.objects.create(
        product=product,
        quantity=quantity,
        total_amount=product.price * quantity,
        stripe_payment_id=checkout_session.id,
        paid=False,
    )

    return redirect(checkout_session.url)
    
def success(request):
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    order = Order.objects.get(stripe_payment_id=session.id)
    order.paid = True
    order.save()

    return redirect("home")

def cancel(request):
    return render(request, "store/cancel.html")
