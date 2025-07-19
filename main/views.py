from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Listing, LikedListing
from django.contrib import messages
from .forms import ListingForm
from users.forms import LocationForm
from django.core.mail import send_mail


#Filter import
from .filters import ListingFilter

# Create your views here.
def main_view(request):
    return render(request, "views/main.html", {"name" : "Automax!:)"})

@login_required
def home_view(request):
    #Retrieve all listing objects to render in home.html as card elements
    listings = Listing.objects.all()
    liked_listing = LikedListing.objects.filter(profile = request.user.profile).values_list('listing')
    Listing_Filter = ListingFilter(request.GET, queryset = listings)
    liked_listing_id = [l[0] for l in liked_listing]
    context = {
        "Listing_Filter" : Listing_Filter,
        "liked_listing_id"  : liked_listing_id
    }
    return render(request, "views/home.html", context)

@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(request, f'{listing.model} Listing Posted Succssfully')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(request, 'An error occured while posting')
    elif request.method == 'GET':
         listing_form = ListingForm()
         location_form = LocationForm()
    return render(request, "views/list.html", {'listing_form' : listing_form, 'location_form' : location_form, })


@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id = id)
        if listing is None:
            raise Exception
        return render(request, "views/listing.html", {'listing' : listing})
    except Exception as e:
        messages.error(request, f'Invalid ID {id} was provided')
        return redirect('home')


@login_required
def edit_view(request, id):
    try:
        edit_listing = Listing.objects.get(id=id)
        if edit_listing is None:
            raise Exception
        if request.POST:
            listing_form = ListingForm(request.POST, request.FILES, instance = edit_listing)
            location_form = LocationForm(request.POST, instance = edit_listing.location)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.info(request, f'Lisitng {id} updated successfully')
                return redirect('home')
            else:
                messages.error(request, f'An error occured while tryig to edit the listing')
                return redirect(request.path)
        else:
            listing_form = ListingForm(instance = edit_listing)
            location_form = LocationForm(instance = edit_listing.location)
        context = {
            'listing_form': listing_form,
            'location_form': location_form
        }
        return render(request, 'views/edit.html', context)
    except Exception as e:
        messages.error(request, f'An error occured while tryig to access the edit page')
        return redirect('home')
    
@login_required
def like_listing_view(request, id):
    listing =  get_object_or_404(Listing, id=id)
    liked_listing, created = LikedListing.objects.get_or_create(profile=request.user.profile, listing = listing)

    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created
    })


@login_required
def inquire_using_email(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        email_subject = f'{request.user.username} is intereseted in {listing.model}'
        email_messgae = f'Hi! {listing.seller.user.username}, {request.user.username} is interested in  your {listing.model}'
        send_mail(email_subject, email_messgae, 'noreply@gmail.com', [listing.seller.user.email], fail_silently=True)
        return JsonResponse({
            "success":True
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success":False,
            "info":e
        })