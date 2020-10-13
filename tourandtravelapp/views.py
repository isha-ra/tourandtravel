from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from urllib.parse import urlparse, parse_qs
from datetime import datetime, date, timedelta
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from .forms import *
# For Client Site
today = date.today()

class BaseMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["subsform"] = SubscriberForm
        context["organization"] = Organization.objects.first()
        context['allpackages'] = ServicePackage.objects.all()
        context['alldestination'] = Service.objects.all()
        return context



class HomeView(BaseMixin, TemplateView):
    template_name = "clienttemplate/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alldestination'] = Service.objects.all()
        context['allimages'] = Image.objects.all()
        context['today'] = today
        # context['offer'] = Offer.objects.filter(
        #     offer_ends__gt=today).order_by('-start_date')
        # context['expoffer'] = Offer.objects.filter(
        #     offer_ends__lt=today).order_by('-start_date')
        context['alloffers'] = Offer.objects.all()

        return context

class AboutView(BaseMixin, TemplateView):
    template_name = "clienttemplate/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alltestimonial'] = Testimonial.objects.all()
        return context

class ServiceView(BaseMixin, TemplateView):
    template_name = "clienttemplate/service.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allservices'] = Service.objects.all()
        context['allteam'] = Team.objects.all()
        return context

class SubscriberCreateView(BaseMixin, SuccessMessageMixin, CreateView):
    template_name = "clienttemplate/subscriber.html"
    form_class = SubscriberForm
    success_url = "/"

    def get_success_message(self, cleaned_data):

        return "Thankyou for subscribing us!!!"

    def form_valid(self, form):

        form_email = form.cleaned_data["email"]

        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        contact_message = "Thanks for subscribing us."
        send_mail(subject,
                  contact_message,
                  from_email,
                  [form_email],
                  fail_silently=False)
        return super().form_valid(form)


class ServiceDetailView(BaseMixin, DetailView):
    template_name = "clienttemplate/servicedetail.html"
    model = Service
    context_object_name = "serviceobject"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["serviceform"] = ServiceForm
        return context


# class PackageView(BaseMixin, TemplateView):
#     template_name = "clienttemplate/package.html"


class ContactView(BaseMixin, SuccessMessageMixin, CreateView):
    template_name = "clienttemplate/contact.html"
    form_class = MessageForm
    success_url = reverse_lazy('tourandtravelapp:contact')
    def get_success_message(self, cleaned_data):
        return "Thankyou for contacting us !!!"
    def form_valid(self, form):
        form_email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        from_email = settings.EMAIL_HOST_USER
        contact_message = "Thankyou for contacting US!!!"
        message = "You have got a new contact message"
        datatuple = (
            (subject, message, from_email, [from_email]),
            (subject, contact_message,
                from_email, [form_email]),
            )
        send_mass_mail(datatuple)
        return super().form_valid(form)


class PackageView(BaseMixin,TemplateView):
    template_name = "clienttemplate/package.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allpackages'] = ServicePackage.objects.all()
        context['today'] = today
        context['alloffers'] = Offer.objects.all()
        return context

class OfferDetailView(BaseMixin, DetailView):
    template_name = "clienttemplate/offerdetail.html"
    model = Offer
    context_object_name = "offerobject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = today
        context["offerform"] = OfferForm

        return context

class PackageDetailView(BaseMixin, DetailView):
    template_name = "clienttemplate/packagedetail.html"
    model = ServicePackage
    context_object_name = "packageobject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["packageform"] = ServicePackageForm
        context["form"] = CommentForm

        return context

class ClientPackageBookView(BaseMixin, CreateView):
    template_name = "clienttemplate/clientpackagebooking.html"
    form_class = PackageBookingForm
    success_url = reverse_lazy("tourandtravelapp:home")

    def form_valid(self, form):
        package_id = self.kwargs["pk"]
        package = ServicePackage.objects.get(id=package_id)
        form.instance.package = package

        return super().form_valid(form)

class EnqueryView(BaseMixin, SuccessMessageMixin, CreateView):
    template_name = "clienttemplate/enquery.html"
    form_class = EnqueryForm
    success_url = reverse_lazy('tourandtravelapp:enquery')
    def get_success_message(self, cleaned_data):
    	return "We will contact you soon!!!"
    def form_valid(self, form):
    	form_email = form.cleaned_data["email"]
    	subject = form.cleaned_data["service"]
    	from_email = settings.EMAIL_HOST_USER
    	contact_message = "Thankyou for contacting us...We will contact you soon!!!"
    	message = "You have got a new enquery message"
    	datatuple = (
    		(subject, message, from_email, [from_email]),
    		(subject, contact_message,
    			from_email, [form_email]),
    		)
    	send_mass_mail(datatuple)
    	return super().form_valid(form)

class AjaxGetPackagesView(TemplateView):
    template_name = "clienttemplate/ajaxgetpackages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serv_id = self.request.GET['service_id']
        serv_obj = Service.objects.get(id=serv_id)
        packages = ServicePackage.objects.filter(service=serv_obj)
        context["relatedpackages"] = packages

        return context

class PackageCommentView(CreateView):
    template_name = "clienttemplate/commentcreate.html"
    form_class = CommentForm
    success_url = reverse_lazy("tourandtravelapp:home")

    def form_valid(self, form):
        package_id = self.kwargs["pk"]
        package = ServicePackage.objects.get(id=package_id)
        form.instance.package = package

        return super().form_valid(form)

    def get_success_url(self):
        package_id = self.kwargs["pk"]
        url_to_redirect = "/package/" + str(package_id) + "/detail/"

        return url_to_redirect


class AlbumView(BaseMixin, TemplateView):
    template_name = "clienttemplate/album.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allalbum'] = Album.objects.all()
        context['allvidoes'] = Video.objects.all()

        return context





        # for admin

class SigninView(FormView):
    template_name = "admintemplate/adminlogin.html"
    form_class = SigninForm
    success_url = reverse_lazy('tourandtravelapp:adminhome')

    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        user = authenticate(username=uname, password=pword)
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, "admintemplate/adminlogin.html",
                          {"error": "Invalid Username or Password",
                           "form": form
                           })

        return super().form_valid(form)

class SignoutView(View):

    def get(self, request):
        logout(request)
        return redirect("/signin/")

        

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/signin/")

        return super().dispatch(request, *args, **kwargs)

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "admintemplate/adminhome.html"