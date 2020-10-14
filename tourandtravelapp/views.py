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

    # forservice start

class AdminServiceListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminservicelist.html"
    queryset = Service.objects.all().order_by('-id')
    context_object_name = "adminservicelist"

class AdminServiceCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminservicecreate.html"
    form_class = ServiceForm
    success_url = reverse_lazy('tourandtravelapp:adminservicelist')


class AdminServiceUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminservicecreate.html"
    form_class = ServiceForm
    model = Service
    success_url = reverse_lazy('tourandtravelapp:adminservicelist')


class AdminServiceDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminservicedelete.html"
    model = Service
    success_url = reverse_lazy('tourandtravelapp:adminservicelist')


# forservice end

# service package start
class AdminServicePackageListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminservicepackagelist.html"
    queryset = ServicePackage.objects.all().order_by('-id')
    context_object_name = "adminservicepackagelist"

class AdminServicePackageCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminservicepackagecreate.html"
    form_class = ServicePackageForm
    success_url = reverse_lazy('tourandtravelapp:adminservicepackagelist')


class AdminServicePackageUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminservicepackagecreate.html"
    form_class = ServicePackageForm
    model = ServicePackage
    success_url = reverse_lazy('tourandtravelapp:adminservicepackagelist')


class AdminServicePackageDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminservicepackagedelete.html"
    model = ServicePackage
    success_url = reverse_lazy('tourandtravelapp:adminservicepackagelist')

# service package end

# team start
class AdminTeamListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminteamlist.html"
    queryset = Team.objects.all().order_by('-id')
    context_object_name = "adminteamlist"


class AdminTeamCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminteamcreate.html"
    form_class = TeamForm
    success_url = reverse_lazy('tourandtravelapp:adminteamlist')


class AdminTeamUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminteamcreate.html"
    form_class = TeamForm
    model = Team
    success_url = reverse_lazy('tourandtravelapp:adminteamlist')


class AdminTeamDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminteamdelete.html"
    model = Team
    success_url = reverse_lazy('tourandtravelapp:adminteamlist')


# team end

# offer start
class AdminOfferListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminofferlist.html"
    queryset = Offer.objects.all().order_by('-id')
    context_object_name = "adminofferlist"


class AdminOfferCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminoffercreate.html"
    form_class = OfferForm
    success_url = reverse_lazy('tourandtravelapp:adminofferlist')


class AdminOfferUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminoffercreate.html"
    form_class = OfferForm
    model = Offer
    success_url = reverse_lazy('tourandtravelapp:adminofferlist')


class AdminOfferDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminofferdelete.html"
    model = Offer
    success_url = reverse_lazy('tourandtravelapp:adminofferlist')

# offerend

# subscriber start
class AdminSubscriberListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminsubscriberlist.html"
    queryset = Subscriber.objects.all().order_by('-id')
    context_object_name = "adminsubscriberlist"


class AdminSubscriberCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminsubscribercreate.html"
    form_class = SubscriberForm
    success_url = reverse_lazy('tourandtravelapp:adminsubscriberlist')


class AdminSubscriberUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminsubscribercreate.html"
    form_class = SubscriberForm
    model = Subscriber
    success_url = reverse_lazy('tourandtravelapp:adminsubscriberlist')


class AdminSubscriberDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminsubscriberdelete.html"
    model = Subscriber
    success_url = reverse_lazy('tourandtravelapp:adminsubscriberlist')

# subscriber end

# Testimonial start
class AdminTestimonialListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/admintestimoniallist.html"
    queryset = Testimonial.objects.all().order_by('-id')
    context_object_name = "admintestimoniallist"


class AdminTestimonialCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/admintestimonialcreate.html"
    form_class = TestimonialForm
    success_url = reverse_lazy('tourandtravelapp:admintestimoniallist')


class AdminTestimonialUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/admintestimonialcreate.html"
    form_class = TestimonialForm
    model = Testimonial
    success_url = reverse_lazy('tourandtravelapp:admintestimoniallist')


class AdminTestimonialDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/admintestimonialdelete.html"
    model = Testimonial
    success_url = reverse_lazy('tourandtravelapp:admintestimoniallist')

# Testimonial end

# album start

class AdminAlbumListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminalbumlist.html"
    queryset = Album.objects.all().order_by('-id')
    context_object_name = "adminalbumlist"


class AdminAlbumCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminalbumcreate.html"
    form_class = AlbumForm
    success_url = reverse_lazy('tourandtravelapp:adminalbumlist')

    def form_valid(self, form):
        album = form.save()
        images = self.request.FILES.getlist("images")
        for image in images:
            Image.objects.create(album=album, image=image, caption="")

        return super().form_valid(form)


class AdminAlbumUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminalbumcreate.html"
    form_class = AlbumForm
    model = Album
    success_url = reverse_lazy('tourandtravelapp:adminalbumlist')


class AdminAlbumDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminalbumdelete.html"
    model = Album
    success_url = reverse_lazy('tourandtravelapp:adminalbumlist')

    # album end

    # image start
class AdminImageListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminimagelist.html"
    queryset = Image.objects.all().order_by('-id')
    context_object_name = "adminimagelist"


class AdminImageCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminimagecreate.html"
    form_class = ImageForm
    success_url = reverse_lazy('tourandtravelapp:adminimagelist')


class AdminImageUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminimagecreate.html"
    form_class = ImageForm
    model = Image
    success_url = reverse_lazy('tourandtravelapp:adminimagelist')


class AdminImageDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminimagedelete.html"
    model = Image
    success_url = reverse_lazy('tourandtravelapp:adminimagelist')

    # image end


    # Video start
class AdminVideoListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminvideolist.html"
    queryset = Video.objects.all().order_by('-id')
    context_object_name = "adminvideolist"


class AdminVideoCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminvideocreate.html"
    form_class = VideoForm
    success_url = reverse_lazy('tourandtravelapp:adminvideolist')

    def form_valid(self, form):
        video_url = form.cleaned_data['link']
        print(video_url)
        url_data = urlparse(video_url)
        print(url_data)
        query = parse_qs(url_data.query)
        print(query, "**************")
        video_id = query.get("v")[0]
        print(video_id)
        form.instance.link = video_id

        return super().form_valid(form)


class AdminVideoUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminvideocreate.html"
    form_class = VideoForm
    model = Video
    success_url = reverse_lazy('tourandtravelapp:adminvideolist')

    def form_valid(self, form):
        video_url = form.cleaned_data['link']
        url_data = urlparse(video_url)
        query = parse_qs(url_data.query)
        print(query, "**************")
        if "v" in query:
            video_id = query["v"][0]
            print(video_id)
            form.instance.link = video_id

        return super().form_valid(form)


class AdminVideoDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminvideodelete.html"
    model = Video
    success_url = reverse_lazy('tourandtravelapp:adminvideolist')
# video end
# enquery start

class AdminEnqueryListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminenquerylist.html"
    queryset = Enquery.objects.all().order_by('-id')
    context_object_name = "adminenquerylist"


class AdminEnqueryCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminenquerycreate.html"
    form_class = EnqueryForm
    success_url = reverse_lazy('tourandtravelapp:adminenquerylist')


class AdminEnqueryUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminenquerycreate.html"
    form_class = EnqueryForm
    model = Enquery
    success_url = reverse_lazy('tourandtravelapp:adminenquerylist')


class AdminEnqueryDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminenquerydelete.html"
    model = Enquery
    success_url = reverse_lazy('tourandtravelapp:adminenquerylist')

    # enqury end

    # message start
class AdminMessageListView(AdminRequiredMixin, ListView):
    template_name = "admintemplate/adminmessagelist.html"
    queryset = Message.objects.all().order_by('-id')
    context_object_name = "adminmessagelist"


class AdminMessageCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplate/adminmessagecreate.html"
    form_class = MessageForm
    success_url = reverse_lazy('tourandtravelapp:adminmessagelist')


class AdminMessageUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplate/adminmessagecreate.html"
    form_class = MessageForm
    model = Message
    success_url = reverse_lazy('tourandtravelapp:adminmessagelist')


class AdminMessageDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "admintemplate/adminmessagedelete.html"
    model = Message
    success_url = reverse_lazy('tourandtravelapp:adminmessagelist')

    # message end