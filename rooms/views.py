from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django_countries import countries
from django.core.paginator import Paginator
from . import models as room_models
from . import forms as room_forms


class HomeView(ListView):

    """ Home View Definition """

    model = room_models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"


class RoomDetailView(DetailView):

    """ Room Detail View Definition """

    model = room_models.Room


class SearchView(View):
    def get(self, request):
        context = {}
        country = request.GET.get("country")
        if country:
            form = room_forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                house_rules = form.cleaned_data.get("house_rules")

                filter_args = {}
                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type__pk"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book:
                    filter_args["instant_book"] = True

                if superhost:
                    filter_args["host__superhost"] = True
                
                for item in amenities:
                    filter_args["amenities"] = item
            
                for item in facilities:
                    filter_args["facilities"] = item
                
                for item in house_rules:
                    filter_args["house_rules"] = item

                print(filter_args)

                rooms = room_models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(rooms, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                context["rooms"] = rooms
        else:
            form = room_forms.SearchForm()

        context["form"] = form

        return render(request, "rooms/room_search.html", context=context)

# def search(request):
#     city = str.capitalize(request.GET.get("city", "Anywhere"))
#     selected_country = request.GET.get("country", "KR")
#     selected_room_type = int(request.GET.get("room_type", 0))
#     price = request.GET.get("price", 0)
#     guests = request.GET.get("guests", 0)
#     beds = request.GET.get("beds", 0)
#     bedrooms = request.GET.get("bedrooms", 0)
#     baths = request.GET.get("baths", 0)
#     selected_amenities = request.GET.getlist("amenities")
#     selected_facilities = request.GET.getlist("facilities")
#     selected_house_rules = request.GET.getlist("house_rules")
#     instant = bool(request.GET.get("instant", False))
#     superhost = bool(request.GET.get("superhost", False))

#     form = {
#         "city": city,
#         "selected_country": selected_country,
#         "selected_room_type": selected_room_type,
#         "price": price,
#         "guests": guests,
#         "beds": beds,
#         "bedrooms": bedrooms,
#         "baths": baths,
#         "selected_amenities": selected_amenities,
#         "selected_facilities": selected_facilities,
#         "selected_house_rules": selected_house_rules,
#         "instant": instant,
#         "superhost": superhost,
#     }

#     room_types = room_models.RoomType.objects.all()
#     amenities = room_models.Amenity.objects.all()
#     facilities = room_models.Facility.objects.all()
#     house_rules = room_models.HouseRule.objects.all()
#     choices = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#         "house_rules": house_rules,
#     }

#     filter_args = {}
#     if city != "Anywhere":
#         filter_args["city__startswith"] = city

#     filter_args["country"] = selected_country

#     if selected_room_type != 0:
#         filter_args["room_type__pk"] = selected_room_type

#     if price != 0:
#         filter_args["price__lte"] = price

#     if guests != 0:
#         filter_args["guests__gte"] = guests

#     if beds != 0:
#         filter_args["beds__gte"] = beds

#     if bedrooms != 0:
#         filter_args["bedrooms__gte"] = bedrooms

#     if baths != 0:
#         filter_args["baths__gte"] = baths

#     if instant:
#         filter_args["instant_book"] = True

#     if superhost:
#         filter_args["host__superhost"] = True

#     if len(selected_amenities) > 0:
#         for item in selected_amenities:
#             filter_args["amenities__pk"] = int(item)

#     if len(selected_facilities) > 0:
#         for item in selected_facilities:
#             filter_args["facilities__pk"] = int(item)

#     if len(selected_house_rules) > 0:
#         for item in selected_house_rules:
#             filter_args["house_rules__pk"] = int(item)

#     print(filter_args)

#     rooms = room_models.Room.objects.filter(**filter_args)

#     print(rooms)

#     context = {
#         **form, **choices, "rooms": rooms,
#     }

#     return render(request, "rooms/room_search.html", context=context)
