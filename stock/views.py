from stock.forms import add_asset_form
from django.shortcuts import render
from django.http import HttpResponse
from .models import Member, Profile, Asset
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import add_asset_form, remove_asset_form, UserProfileForm
from django.db import models

# Create your views here.
def index(request):
    asc_pe_list = Member.objects.order_by('pe_ratio')[:50]
    desc_pe_list = Member.objects.order_by('eps')[:50]
    template = loader.get_template('stock/landing.html')
    context = {
        'asc_pe_list': asc_pe_list,
        'desc_pe_list': desc_pe_list
    }
    return HttpResponse(template.render(context,request))

def pie_chart(request):
    labels = []
    data = []
    members = {}
    avg_pe = 0
    for member in Member.objects.all():
        members[member.ticker]= member.price

    if request.user.is_authenticated:
        queryset = request.user.profile.assets.order_by('-quantity')
        count = 0
        for asset in queryset:
            try:
                value = float(asset.quantity) * float(members[asset.name])
                labels.append(asset.name)
                data.append(float("{:.2f}".format(value)))
                stock = Member.objects.get(ticker=asset.name)
                try:
                    avg_pe += stock.pe_ratio #make it weighted by the value of your assets 
                    count += 1
                except TypeError:
                    pass
            except KeyError:
                asset.delete()
                return redirect('not_found')
        if(count > 0):
            avg_pe = avg_pe/count
    return render(request, 'home.html', {'labels': labels,'data': data,'user': request.user, 'avg_pe':avg_pe})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid(): #and profile_form.is_valid():
            user = form.save()

            profile1 = profile_form.save(commit=False)
            profile1.user = user
            profile1.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm()
    return render(request, 'signup.html', {'form': form, 'profile_form' : profile_form})


def add_asset(request):
    if request.method == 'POST':
        form = add_asset_form(request.POST)
        user_profile = request.user.profile
        if form.is_valid():
            asset = form.save()
            asset.name = asset.name.upper()
            asset.save()
            for member in Member.objects.all():
                if member.ticker == asset.name:
                    asset.last_updated = member.last_updated
                    asset.save()
                    if user_profile.total is None:
                        user_profile.total = 0
                    user_profile.total += (asset.quantity * member.price)
                    user_profile.save()  
            for object in user_profile.assets.all():
                if object.name == asset.name:
                    object.quantity += asset.quantity
                    object.save()
                    return redirect('home')
            user_profile.assets.add(asset)      
        return redirect('home')
    else:
        form = add_asset_form()
    context = {'form': form,}
    return render(request, 'add_asset.html', context)


def remove_asset(request):
    if request.method == 'POST':
        form = remove_asset_form(request.POST)
        user_profile = request.user.profile
        if form.is_valid():
            asset = form.save()
            asset.name = asset.name.upper()
            asset.save()
            for object in user_profile.assets.all():
                if object.name == asset.name:
                    if(asset.quantity is None):
                        for member in Member.objects.all():
                            if(member.ticker == asset.name):
                                user_profile.total -= (member.price * object.quantity)
                                user_profile.save()
                        object.delete()
                    elif(object.quantity - asset.quantity) <= 0:
                        for member in Member.objects.all():
                            if(member.ticker == asset.name):
                                user_profile.total -= (member.price * object.quantity)
                                user_profile.save()
                        object.delete()
                    else:
                        for member in Member.objects.all():
                            if(member.ticker == asset.name):
                                user_profile.total -= (member.price * asset.quantity)
                                user_profile.save()
                        object.quantity -= asset.quantity
                        object.save()
                    return redirect('home')
        return redirect('home')
    else:
        form = remove_asset_form()
    context = {'form': form,}
    return render(request, 'remove_asset.html', context)

def not_found(request):
    context = {}
    return render(request, 'not_found.html', context)

def info(request):
    context = {}
    return render(request, 'info.html', context)

