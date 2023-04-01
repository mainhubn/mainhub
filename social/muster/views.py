from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Profile,Meep,Room,Message
from .forms import MeepForm,SignUpForm,ProfilePicForm,MeepPicForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all()

        form = MeepForm(request.POST or None,request.FILES or None)
        Meepprofile_form = MeepPicForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid() and Meepprofile_form.is_valid():

                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                Meepprofile_form.save()

                messages.success(request,("Your Meep have been Posted!"))
                return redirect('home')
            
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request,'home.html',{"meeps":meeps,"form":form,"profiles":profiles,"Meepprofile_form":Meepprofile_form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request,'home.html',{"meeps":meeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request,("You Must be logged in to view this page"))
        return redirect('home')

def profile(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request,"profile.html",{"profile":profile,"meeps":meeps})
    else:
        messages.success(request,("You Must be logged in to view this page"))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("You Have Been Logged In"))
            return redirect('home')  
        else: 
            messages.success(request,("There Was an Error loging in. Please try again..."))
            return redirect('login')        
    else:
        return render(request,"login.html",{})

def logout_user(request):
    logout(request)
    messages.success(request,("You Have Been Logged Out."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
#            first_name = form.cleaned_data['first_name']
#            last_name = form.cleaned_data['last_name']
#            email = form.cleaned_data['email']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You Have Sucssesfully Registerd | Welcome!"))
            return redirect('home')
    return render(request,"register.html",{"form":form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForm(request.POST or None,request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None,instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request,current_user)
            messages.success(request,("Your Profile Has Been Updated"))
            return redirect('home')
        return render(request,'update_user.html',{"user_form":user_form,"profile_form":profile_form})
    else:
        messages.success(request,("You Must be logged in to view this page"))
        return redirect('home')

def hHomepage(request):
    usernam = Profile.objects.get(user=request.user)
    username = usernam.user
    room1 = request.POST.get('chatid',None)
    room2 = usernam.user
    try:
        room = f'{room1} {room2}'
        get_room = Room.objects.get(room_name=room)
        return redirect('room', room_name=room,username=username)
    except Room.DoesNotExist:
        try:
            room = f'{room2} {room1}'
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room,username=username)
        except Room.DoesNotExist:
            new_room = Room(room_name = room)
            new_room.save()
            return redirect('room', room_name=room,username=username)

def MessageView(requset,room_name,username):
    usernam = Profile.objects.get(user=requset.user)
    usernamee = usernam.user
    usernamef = f"{usernamee}"
    get_room=Room.objects.all()
    c = []
    z=[]
    geta_room = Room.objects.filter()
    for i in get_room:
        c.append(f"{i}")
        b = f"{i}"
        v = b.split()
        v.remove(f'{usernamef}')
        z.extend(v)

    user_f = Profile.objects.exclude(user = requset.user)
    get_room = Room.objects.get(room_name=room_name)

    if requset.method == "POST":
        message = requset.POST['message']
        print(message)
        
        new_message = Message(room=get_room,sender=username,message=message)
        new_message.save()

    get_room = Room.objects.get(room_name=room_name)
    get_messages=Message.objects.filter(room=get_room)
    context = {
        "messagess": get_messages,
        "user": username,
        "profiles":user_f,
        "user":username,
        "f_list":z,
    }

    return render(requset,'message.html',context)
def user_sb(request):
    if request.user.is_authenticated:
        usernam = Profile.objects.get(user=request.user)
        usernamee = usernam.user
        username = f"{usernamee}"
        get_room=Room.objects.all()
        c = []
        z=[]
        geta_room = Room.objects.filter()


        for i in get_room:
            c.append(f"{i}")
            b = f"{i}"
            v = b.split()
            v.remove(f"{username}")
            z.extend(v)

        user_f = Profile.objects.exclude(user = request.user)
        


        return render(request,'user_sb.html',{"profiles":user_f,"user":username,"f_list":z})
    else:
        messages.success(request,("You Must be logged in to view this page"))
        return redirect('home')
