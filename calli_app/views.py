from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from calli_app.models import product,cart,order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail



# Create your views here.

def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def workshop(request):
    return render(request,'workshop.html')

def form_cont(request):
    return render(request,'form_cont.html')

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}  
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="fields cannot be empty"
            return render(request,'register.html',context)
        elif upass != ucpass:
            context['errmsg']="password and confirm password didnt match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass) #encrypted format
                u.save()
                context['success']='user register successfully'
                return render(request,'register.html',context)
                #return HttpResponse("User created successfully")
            except Exception:
                context['errmsg']='username already exist'
                return render(request,'register.html',context)

    else:
        return render(request,'register.html')
        
def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="fields cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            #return HttpResponse("in else part")
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg']="Invalid username and password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/home')

def gifts(request):
    context={}
    p=product.objects.filter(is_active=True)
    context['product']=p
    return render(request,'gifts.html',context)


def ser(request):
    return render(request,'ser.html')

def form_cont(request):
    return render(request,'form_cont.html')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1&q2)
    context={}
    context['product']=p
    return render(request,'gifts.html',context)


def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(pid)
        #print(userid)
        u=User.objects.filter(id=userid)
        print(u[0])
        p=product.objects.filter(id=pid)
        print(p[0])
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context['products']=p
        if n==1:
            context['msg']='Selected product is already added in CART!!'
        else:
            c=cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added successfully to cart!!"
        return render(request,'gifts.html',context)
        #return HttpResponse("data is fetch")
    else:
        return redirect('/login')

def viewcart(request):
    if request.user.is_authenticated: #if user logged in then if part
        c=cart.objects.filter(uid=request.user.id)
        np=len(c)
        s=0
        for x in c:
            s=s+ x.pid.price * x.qty
        print(s)
        context={}
        context['products']=c
        context['total']=s
        context['n']=np
        return render(request,'cart.html',context)
    else:
        return redirect('/login')

def remove(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty + 1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    #return HttpResponse("quantity")
    return redirect('/viewcart')   


def placeorder(request):
    userid=request.user.id
    c=cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    for x in c:
        o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=order.objects.filter(uid=request.user.id)
    context={}
    context['products']=orders
    np=len(orders)
    s=0
    for x in orders:
        s= s+ x.pid.price * x.qty
    context['total']=s
    context['n']=np
    #return HttpResponse("inplace")
    return render(request,'placeorder.html',context)

def makepayment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+ x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_elANQGSwVPX1CL", "hRpQD7Qq7f4OryOsGvUPBxW5"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    uname=request.user.username
    context['uname']=uname
    context['data']=payment
    return render(request,'pay.html',context)
    #return HttpResponse('in ,makje pa]y')

def sendusermail(request,uname): 
    msg="order details are:"
    send_mail(
        "Ekart - order placed successfully ",
        msg,
        "order details are:.",
        "from@example.com",
        [uname],
        fail_silently=False,
    )
    return HttpResponse("mail success")