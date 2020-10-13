from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Organization, Service, ServicePackage, Booking, Comment, Offer,
                     Team, Subscriber, Testimonial, Album, Image, Video, Enquery, Message])
