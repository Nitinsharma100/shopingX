from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Cart,OrderPlaced,Product,CustomerProfileform
from .forms import CustomerRegistrationform
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})
    

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})


from django.urls import reverse


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        # Optionally, you can increment the quantity if it's already in the cart
        cart_item.quantity += 1
        cart_item.save()
    
    # Redirect to the cart page
    return redirect(reverse('showcart'))


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0

        if cart.exists():  # Check if the cart has items
            for p in cart:
                temp_amount = (p.quantity * p.product.discount_price)
                amount += temp_amount
            
            total_amount = amount + shipping_amount  # Calculate total amount including shipping

            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')  # Render empty cart template
    else:
        return render(request, 'app/login.html')  # Redirect unauthenticated users to login

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discount_price)
            amount += temp_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        try:
            # Find and delete the specific cart item
            cart_item = Cart.objects.get(product__id=prod_id, user=request.user)
            cart_item.delete()
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found in the cart'}, status=404)
        
        # Recalculate the total cart amount after deletion
        amount = 0.0
        shipping_amount = 70.0
        cart_products = Cart.objects.filter(user=request.user)
        
        for cart_item in cart_products:
            temp_amount = cart_item.quantity * cart_item.product.discount_price
            amount += temp_amount
        
        # If the cart is empty, set shipping to 0
        if amount == 0:
            shipping_amount = 0.0
        
        # Return the updated amounts
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

            



def buy_now(request):
    return render(request, 'app/buynow.html')


def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    user = request.user
    order_placed = OrderPlaced.objects.filter(user=user)
    return render(request, 'app/orders.html', {'order_placed': order_placed})




def mobile(request, data=None):
    mobiles = Product.objects.none()  

    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data in ['Redmi', 'Samsung']:  # Filter by brand
        mobiles = Product.objects.filter(category='M', brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M', discount_price__lt=10000)  # Filter by price below 10000
    elif data == 'above':
        mobiles = Product.objects.filter(category='M', discount_price__gt=10000)  # Filter by price below 10000

    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptop(request,data=None):
    if data is None:
        laptops = Product.objects.filter(category='L')
    elif data in ['Hp', 'Acer']:  # Filter by brand
        laptops = Product.objects.filter(category='L', brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L', discount_price__lt=30000)  # Filter by price below 10000
    elif data == 'above':
        laptops = Product.objects.filter(category='L', discount_price__gt=30000)  # Filter by price below 10000

    return render(request, 'app/laptop.html', {'laptops': laptops})
   



# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class customerregistrationform(View):
    def get(self,request):
        form=CustomerRegistrationform()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationform(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    for cart_item in cart_items:
        temp_amount = cart_item.quantity * cart_item.product.discount_price
        amount += temp_amount

    totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {
        'addresses': addresses,  # Pass the queryset of addresses
        'totalamount': totalamount,
        'cart_items': cart_items
    })

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileform()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form=CustomerProfileform(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
from django.shortcuts import get_object_or_404, redirect

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = get_object_or_404(Customer, id=custid, user=user)
    cart_items = Cart.objects.filter(user=user)
    
    for item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=item.product,
            quantity=item.quantity
        )
        item.delete()
    return redirect('orders') 

