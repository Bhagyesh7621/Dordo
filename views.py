from multiprocessing import context
from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout
from med.form import CustomeraddressForm, PassChangeForm, SigninForm, SignupForm, UserProfileChangeForm
from django.contrib import messages

from med.models import Cart, CustomeraddressModel, MainCategories, Order, Product,SubCategories, Wishlist 
import razorpay


# Create your views here.
def IndexView(request):
    data = MainCategories.objects.all()
    subdata = SubCategories.objects.all()
    cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {'data':data,'subdata':subdata,'cart_count':cart_count}
    return render(request, 'index.html',context)

def LoginView(request):
    return render(request, 'login.html')

def SignupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            usrname= form.cleaned_data['username']
          
            form.save() 
            messages.success(request,f'{usrname} Successfully Registred')
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
        context = {'form': form, }
    return render(request, 'signup.html', context)




def SigninView(request):
    form = SigninForm()
    if request.method == 'POST':

        uname = request.POST['uname']
        upass = request.POST['upass']
        user = authenticate(username=uname, password=upass)
        if user is None:
            messages.error(request, 'Please Enter Correct Credinatial')
            return redirect('/signin/')
        else:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('/index/')
    else:
        if request.user.is_authenticated:
            return redirect('/index/')
        else:
            return render(request, 'signin.html', {'form': form})


def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'you are successfully logout')
        return redirect('/signin/')
    else:
        messages.info(request, 'please login first')
    return redirect('/signin/')


# Start Shop View

def ShopView(request):
    data = Product.objects.all()
    cart_count = Cart.objects.filter(user=request.user).count()
    context = {'data':data,'cart_count':cart_count}
    
    return render(request, 'shop.html',context)
# end Shop View

def ChangePassView(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PassChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password Successfully Changed')
        else:
            form = PassChangeForm(user=request.user)

        context = {'form': form, }
        return render(request, 'passchange.html', context)
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/signin/')


# profile
def ProfileView(request):
    if request.user.is_authenticated:
        form = UserProfileChangeForm(instance=request.user)
        context = {'form': form}
        if request.method == 'POST':
            form = UserProfileChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                get_user = form.cleaned_data['username']
                messages.info(request, f'{get_user} - successfully updates')
                return redirect('/profile/')
        else:
            form = UserProfileChangeForm(instance=request.user)
        context = {'form': form, }
        return render(request, 'profile.html', context)


# Start Contact View

def ContactView(request):
    
    return render(request, 'contact.html')

# end Contact View

#Start abiut View

def AboutView(request):

    return render(request, 'about.html')

#End About View

def ProductInfoView(request, id):
    GetProduct = Product.objects.get(id=id)
    context={'GetProduct':GetProduct}
    return render(request,'productinfo.html',context)


def CartView(request):        
    cart_count = Cart.objects.filter(user=request.user).count()
    cart_items = Cart.objects.filter(user=request.user)

    sub_total = 0
    ship_charge = 70
    GST = 120
    grand_total = 0
    # get data for order
    user = request.user
    get_address_id = request.GET.get('add')
    print(get_address_id, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    for i in cart_items:
        
        sub_total += i.prod_total()
        grand_total = sub_total + ship_charge + GST
        GST = grand_total*0.18
        print(grand_total, "ggggggggggggggggggggggggggggg")
    
    # sub_total = 0
    # ship_charge = 30
    # GST = 120
    # grand_total = 0
    # for i in cart_items:
    #     sub_total += i.prod_total()
    # grand_total = sub_total + ship_charge + GST

    context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,'ship_charge': ship_charge, 'GST': GST, 'grand_total': grand_total,}
    return render(request, 'cart.html', context)

def Add_to_cartView(request, id):
    user = request.user
    prod = Product.objects.get(id=id)
    item_exist = Cart.objects.filter(product=prod).exists()

    if item_exist:
        get_item = Cart.objects.get(product__id=id)
        get_item.quantity += 1
        get_item.save()
        return redirect('/cart/')
    else:
        product = Product.objects.get(id=id)
    Cart(user=user, product=product).save()
    return redirect('/index/')



def WishListView(request):        
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    cart_count = Cart.objects.filter(user=request.user).count()


    context = {'wishlist_count': wishlist_count, 'wishlist_items': wishlist_items,'cart_count':cart_count}
    return render(request, 'wishlist.html', context)

def Add_to_wishlist(request, id):
    user = request.user
    prod = Product.objects.get(id=id)
    item_exist = Wishlist.objects.filter(product=prod).exists()

    if item_exist:
        get_item = Wishlist.objects.get(product__id=id)
        get_item.quantity += 1
        get_item.save()
        return redirect('/wishlist/')
    else:
        product = Product.objects.get(id=id)
    Wishlist(user=user, product=product).save()
    return redirect('/index/')


def pluse_quantity(request, id):
    get_item = Cart.objects.get(id=id)
    if get_item:
        get_item.quantity += 1
        get_item.save()
        return redirect('/cart/')


def minus_quantity(request, id):
    get_item = Cart.objects.get(id=id)
    if get_item:
        get_item.quantity -= 1
        get_item.save()
        if get_item.quantity == 0:
            get_item.delete()
        return redirect('/cart/')


def DeleteView(request, id):
    get_item = Cart.objects.get(id=id)
    get_item.delete()
    get_name = get_item.product.name
    print(get_name)
    messages.error(request, f'{get_name} - Successfully delete')
    return redirect('/cart/')

def clearcart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_items.delete()
    messages.error(request, 'Cart Successfully Cleared')
    return redirect('/cart/')

def ListDeleteView(request, id):
    get_item = Wishlist.objects.get(id=id)
    get_item.delete()
    get_name = get_item.product.name
    print(get_name)
    messages.error(request, f'{get_name} - Successfully delete')
    return redirect('/wishlist/')


def CustomerAddressView(request):
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    if request.user.is_authenticated:
        form = CustomeraddressForm(instance=request.user)
        context = {'form': form}
        if request.method == 'POST':
            form = CustomeraddressForm(request.POST)
            if form.is_valid():
                fm = form.save(commit=False)
                fm.user = request.user
                fm.save()

                messages.info(request, 'Address Successfully Added')
                return redirect('/address/')
        else:
            form = CustomeraddressForm(instance=request.user)

        context = {'form': form, 'all_address': all_address}
        return render(request, 'address.html', context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/signin/')


#CustAdd Update Start

def UpdateaddressView(request, id):
    address = CustomeraddressModel.objects.all()  # Show data of Student Table
    set_address = CustomeraddressModel.objects.get(id=id)
    if request.method == 'POST':
        form = CustomeraddressForm(
            request.POST, request.FILES, instance=set_address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student Successfully Updated')
            return redirect('/address/')
    else:
        form = CustomeraddressForm(instance=set_address)
    context = {'form': form, 'address': address}
    return render(request, 'address.html', context)


#Custadd Update End

#Cust add delete start

def AddressDeleteView(request, id):
    address = CustomeraddressModel.objects.get(id=id)
    address.delete()
    messages.error(request, 'address Successfully delete')
    return redirect('/address/')

#custs add delete end


# Checkout view start

def CheckoutView(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    cart_items = Cart.objects.filter(user=request.user)
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    # totals count -----
    sub_total = 0
    ship_charge = 70
    GST = 120
    grand_total = 0
    # get data for order
    usr = request.user
    get_address_id = request.GET.get('add')
    print(get_address_id, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    for i in cart_items:
        sub_total += i.prod_total()
        grand_total = sub_total + ship_charge + GST
        print(grand_total, "ggggggggggggggggggggggggggggg")
    # payment Start
    amount = (grand_total)*100 
    client = razorpay.Client(
        auth=("rzp_test_cPZYCowWptvFRP", "Dp4CbudriiriMfoW20L9nrav"))
    payment = client.order.create(
        {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    # payment End
    if get_address_id:
        address = CustomeraddressModel.objects.get(id=get_address_id)
        for i in cart_items:
            order_data = Order(
                user=usr,
                customer=address,
                product=i.product,
                quantity=i.quantity

            )
            order_data.save()
        cart_items.delete()
    context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,
               'ship_charge': ship_charge, 'GST': GST, 'grand_total': grand_total, 'all_address': all_address,
               'payment': payment}
    return render(request, 'checkout.html', context)



#checkout view end

def OrderView(request):
    cust_order = Order.objects.filter(user=request.user)
    context = {'cust_order': cust_order}
    return render(request, 'order.html', context)



#All Product view start



def AllproductView(request):
    all_categories = SubCategories.objects.all()
    all_products = Product.objects.all()
    cart_count = Cart.objects.filter(user=request.user).count()

    get_cat_id = request.GET.get('catesid')
    if get_cat_id:
        all_products = Product.objects.filter(pcate__id=get_cat_id)

    get_product_name = request.GET.get('byname')
    if get_product_name:
        all_products = Product.objects.filter(
            name__icontains=get_product_name)

    get_category = request.GET.get('catename')
    get_from_price = request.GET.get('startprice')
    get_to_price = request.GET.get('endprice')

    get_prodname = request.GET.get('pordname')
    # print(get_category,get_from_price,get_to_price,get_prodname)
    if get_category and get_from_price == '' and get_to_price == '' and get_prodname == '':
        all_products = Product.objects.filter(pcate__name=get_category)
    if get_category and get_from_price and get_to_price == '' and get_prodname == '':
        all_products = Product.objects.filter(
            pcate__name=get_category, sell_price__gte=int(get_from_price))
    if get_category and get_from_price and get_to_price and get_prodname == '':
        all_products = Product.objects.filter(pcate__name=get_category, sell_price__gte=int(
            get_from_price), sell_price__lte=int(get_to_price))
    if get_category and get_from_price and get_to_price and get_prodname:
        all_products = Product.objects.filter(pcate__name__icontains=get_category, sell_price__gte=int(
            get_from_price), sell_price__lte=int(get_to_price), name__icontains=(get_prodname))
    context = {'all_categories': all_categories, 'all_products': all_products,
               'cart_count': cart_count}
    return render(request, 'allproducts.html', context)



#All product view end