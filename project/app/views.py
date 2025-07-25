from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from.models import Register,Product, Cart, OrderItem,Order,Feedback
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login as auth_login
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, Order, OrderItem




def func(request):
    return render(request,'home.html')


def func1(request):
    if request.method == 'POST':
        FirstName=request.POST.get("FirstName")
        LastName=request.POST.get("LastName")
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        usertype=request.POST.get('usertype')
        if Register.objects.filter(email=email).exists():
            print("Email exists")
        else:
            password=make_password(password)
            user = Register.objects.create(FirstName=FirstName,LastName=LastName,phone=phone,email=email,username=username,password=password,usertype=usertype)
            print("Registered succesfully")
            # Auto-login after registration
            from django.contrib.auth import login as auth_login, authenticate
            user = authenticate(request, username=username, password=request.POST.get('password'))
            if user:
                auth_login(request, user)
                # Handle pending cart addition
                pending_cart = request.session.pop('pending_cart', None)
                if pending_cart:
                    from .models import Product, Cart
                    product = Product.objects.get(id=pending_cart['product_id'])
                    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
                    cart_item.quantity += int(pending_cart['quantity'])
                    cart_item.save()
                    return redirect('displaycart')
            return redirect('login')
    return render(request,'register.html')
               

def func2(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        print(password)
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            profile=Register.objects.get(username=username)
            request.session['uname']=profile.username
            request.session['ut']=profile.usertype
            print("Login succesful")
            # Handle pending cart addition
            pending_cart = request.session.pop('pending_cart', None)
            if pending_cart:
                from .models import Product, Cart
                product = Product.objects.get(id=pending_cart['product_id'])
                cart_item, created = Cart.objects.get_or_create(user=user, product=product)
                cart_item.quantity += int(pending_cart['quantity'])
                cart_item.save()
                return redirect('displaycart')
            if profile.is_superuser:
                return redirect('view_users')
            else:
                return redirect('profile')
        else:
            print("login succesful")
    return render(request,'login.html')

def func3(request):
    return render(request,'home.html')


@login_required
def func4(request):
    profile = request.user  # This is already your Register instance
    return render(request, 'profile.html', {'profile': profile})

def func5(request):
    logout(request)
    print("Logout sucessfully")
    return redirect('index')

def func6(request):
    users=Register.objects.filter(is_superuser=False)
    return render(request,'view_users.html',{'users':users})
    
def func7(request):
    user=request.user
    profile=Register.objects.get(id=user.id)
    if request.method=='POST':
        FirstName=request.POST.get("FirstName")
        LastName=request.POST.get("LastName")
        phone=request.POST.get('phone')
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        usertype=request.POST.get('usertype')
        if Register.objects.filter(username=username).exclude(id=profile.id).exists():
            print("Username exists")
        else:
            profile.FirstName=FirstName if FirstName else profile.FirstName
            profile.LastName= LastName if LastName else profile.LastName
            profile.phone=phone if phone else profile.phone
            profile.email=email if email else profile.email
            profile.username=username if username else profile.username
            profile.password=make_password(password) if password else profile.password
            profile.usertype=usertype if usertype else profile.usertype
            profile.save()
            print("Updated sucessfully")
            logout(request)
            return redirect('login')
    return render(request,'register.html',{'profile':profile})


def func8(request,id):
    user=Register.objects.get(id=id)
    user.delete()
    print("Deleted")
    return redirect('view_users')

def func9(request):
    if request.method == 'POST':
        name=request.POST.get("name")
        price=request.POST.get("price")
        description=request.POST.get("description")
        warranty=request.POST.get("warranty")
        image = request.FILES.get("image")
        Product.objects.create(name=name,price=price,description=description,warranty=warranty,image=image,seller=request.user)
        print("Product registration sucessful")
        return redirect('display')
    return render(request,'product.html')


def func10(request):
    if request.user.is_authenticated and getattr(request.user, "usertype", None) == "seller":
        products = Product.objects.filter(seller=request.user)
    else:
        products = Product.objects.all()
    return render(request, 'display.html', {'products': products})

from django.shortcuts import get_object_or_404, redirect

def func11(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('display')


'''
*/ def func12(request, product_id=None):
    user=request.user
    product=Product.objects.get(id=user.id)
    if  request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        warranty = request.POST.get("warranty")
        image = request.FILES.get("image")
        if Product.objects.filter(name=name).exclude(id=Product.id).exists():
            print("Product exists")
        else:
            product.name = name if name else product.name
            product.price = price if price else product.price
            product.description = description if description else product.description
            product.warranty = warranty if warranty else product.warranty
            product.image = image if image else product.image
            product.save()
            print("Updated successfully")
        return redirect('display')
    return render(request, 'display.html', {'product': product})
'''

def func12(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        warranty = request.POST.get("warranty")
        image = request.FILES.get("image")

        if Product.objects.filter(name=name).exclude(id=product.id).exists():
            print("Product exists")
        else:
            product.name = name or product.name
            product.price = price or product.price
            product.description = description or product.description
            product.warranty = warranty or product.warranty
            product.image = image or product.image
            product.save()
            print("Updated successfully")

        return redirect('display')

    return render(request, 'editproduct.html', {'product': product})


def func13(request, id):
    product = get_object_or_404(Product, id=id)
    quantity = 1
    if not request.user.is_authenticated:
        # Store intended cart addition in session and redirect to login
        request.session['pending_cart'] = {'product_id': id, 'quantity': quantity}
        return redirect('login')
    if Cart.objects.filter(user=request.user, product=product).exists():
        cart = Cart.objects.get(user=request.user, product=product)
        cart.quantity += quantity
        cart.save()
        print("Quantity updated in cart")
    else:
        Cart.objects.create(user=request.user, product=product, quantity=quantity)
        print("New item added to cart")
    return redirect('displaycart')



@login_required
def func14(request):
    user = request.user
    carts = Cart.objects.filter(user=user).order_by('-added_at')
    total = 0
    for item in carts:
        item.subtotal = item.quantity * item.product.price
        total += item.subtotal
    date_paid = timezone.now()  # or use the actual payment date if available
    return render(request, 'displaycart.html', {
        'cartitems': carts,
        'total': total,
        'date_paid': date_paid,
    })

def func15(request):
    cart=Cart.objects.filter(user=request.user)
    subtotal = 0
    for i in cart:
        subtotal += i.quantity * i.product.price
    print("Subtotal:", subtotal)

    neworder = Order.objects.create(userid=request.user,totalamount=subtotal)

    for i in cart:
        OrderItem.objects.create(orderid=neworder,product=i.product,quantity=i.quantity)
    
    for j in cart:
        j.delete()
    
    return redirect('displayorder')


def func16(request):
    if request.user.usertype == "user":
        orders = Order.objects.filter(userid=request.user).order_by('date')
    else:
        # Get all OrderItems where the product's seller is the current user
        order_items = OrderItem.objects.filter(product__seller=request.user)
        # Get unique order IDs from those order items
        order_ids = order_items.values_list('orderid', flat=True).distinct()
        # Retrieve corresponding orders
        orders = Order.objects.filter(id__in=order_ids).order_by('date')
    
    return render(request, 'displayorder.html', {'displayorder': orders})


def func17(request,id):
    order = Order.objects.get(id=id)
    order_items = OrderItem.objects.filter(orderid=order)
    return render(request,'orderitems.html',{'orderitems':order_items,'order':order})

def func18(request,id):
    order=Order.objects.get(id=id)
    item = OrderItem.objects.filter(orderid=order).first()
    seller = item.product.seller
    if request.method == "POST":
        rating = request.POST.get("Rating")
        message = request.POST.get("Message")
        feedback = Feedback.objects.create(userid=request.user,orderid=order,seller=seller,rating=rating,message=message)
        print("Feedback added successfully")
        return redirect('displayorder')
    return render(request,'feedback.html')


def func19(request,id):
    order = Order.objects.get(id=id)
    feedbacks = Feedback.objects.filter(orderid=order)
    return render(request,'viewfeedback.html',{'feedbacks':feedbacks})


def func20(request):
    feedbacks=Feedback.objects.all()
    return render(request,'viewallfeedbacks.html',{'feedbacks':feedbacks})




@login_required
def paynow(request):
    # Simulate or handle actual payment processing here

    # For now, just show successful message
    return render(request, 'paynow.html', {'payment_success': True})




@login_required
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        # Store intended cart addition in session
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1
        request.session['pending_cart'] = {'product_id': product_id, 'quantity': quantity}
        return redirect('login')
    # User is authenticated, proceed as before
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f"Added {product.name} to cart.")
        return redirect('product_list')
    return redirect('product_list')




@user_passes_test(lambda u: u.is_superuser)
def view_users(request):
    users = Register.objects.all()
    return render(request, 'view_users.html', {'users': users})





@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, id):
    user = get_object_or_404(Register, id=id)
    if not user.is_superuser:  # Prevent deleting other admins
        user.delete()
    return redirect('view_users')


@user_passes_test(lambda u: u.is_superuser)
def admin_user_orders(request, user_id):
    user = get_object_or_404(Register, id=user_id)
    orders = Order.objects.filter(userid=user).order_by('-date')
    return render(request, 'admin_user_orders.html', {'orders': orders, 'viewed_user': user})

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from .models import Product

@user_passes_test(lambda u: u.is_authenticated and u.usertype == "seller")
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        warranty = request.POST.get("warranty")
        image = request.FILES.get("image")
        # Create the product with the current user as seller
        Product.objects.create(
            name=name,
            price=price,
            description=description,
            warranty=warranty,
            image=image,
            seller=request.user
        )
        return redirect('seller_products')  # Redirect to seller's product list
    return render(request, 'add_product.html')

@user_passes_test(lambda u: u.is_authenticated and u.usertype == "seller")
def seller_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'seller_products.html', {'products': products})

from django.contrib.auth.decorators import user_passes_test
from .models import OrderItem

@user_passes_test(lambda u: u.is_authenticated and u.usertype == "seller")
def seller_orders(request):
    order_items = OrderItem.objects.filter(product__seller=request.user)
    return render(request, 'seller_orders.html', {'order_items': order_items})


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

@user_passes_test(lambda u: u.is_authenticated and u.usertype == "seller")
def seller_returns(request):
    returns = OrderItem.objects.filter(product__seller=request.user, returned=True)
    return render(request, 'seller_returns.html', {'returns': returns})


def return_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if item.orderid.userid != request.user:
        return HttpResponseForbidden("You are not allowed to return this item.")
    if request.method == "POST" and not item.returned:
        item.returned = True
        item.return_date = timezone.now()
        item.save()
    return redirect('orderitems', id=item.orderid.id)

def product_detail(request, product_id):
    from .models import Product
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def checkout_all(request):
    if request.method == 'POST':
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return redirect('displaycart')
        order = Order.objects.create(userid=user, totalamount=0)
        total = 0
        for item in cart_items:
            OrderItem.objects.create(orderid=order, product=item.product, quantity=item.quantity)
            total += item.product.price * item.quantity
        order.totalamount = total
        order.save()
        cart_items.delete()
        return redirect('displayorder')
    return redirect('displaycart')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.delete()
    return redirect('displaycart')