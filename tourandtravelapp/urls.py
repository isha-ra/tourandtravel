from django.urls import path
from .views import *

app_name="tourandtravelapp"
urlpatterns = [
# for client urls
	path("",HomeView.as_view(),name="home"),
    path('about/', AboutView.as_view(), name='about'),
    path('service/', ServiceView.as_view(), name='service'),
    path('package/', PackageView.as_view(), name='package'),
    path('contact/', ContactView.as_view(), name='contact'),
    path("subscriber/", SubscriberCreateView.as_view(), name="subscriber"),
    path('package/', PackageView.as_view(), name='package'),
	path('offer/<int:pk>/detail/',
		OfferDetailView.as_view(), name="offerdetail"),
	path('package/<int:pk>/detail/',
         PackageDetailView.as_view(), name="packagedetail"),
	path("service-package/<int:pk>/book/",
         ClientPackageBookView.as_view(), name='clientpackagebook'),
	path('enquery/', EnqueryView.as_view(), name='enquery'),
	path("ajax/service-packages/",
		AjaxGetPackagesView.as_view(), name='ajaxgetpackages'),
	path('package/<int:pk>/comment/',
         PackageCommentView.as_view(), name="packagecomment"),
	path('album/', AlbumView.as_view(), name='album'),
	path('service/<slug:slug>/detail/',
         ServiceDetailView.as_view(), name="servicedetail"),

	# foradmin
	path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('med-admin/home', AdminHomeView.as_view(), name='adminhome'),

    # for adding destination,delete update
    path('med-admin/service/list/',
    	AdminServiceListView.as_view(), name="adminservicelist"),
	path('med-admin/service/create/',
         AdminServiceCreateView.as_view(), name="adminservicecreate"),
	path('med-admin/<int:pk>/edit/',
         AdminServiceUpdateView.as_view(), name="adminserviceupdate"),
    path('med-admin/<int:pk>/delete/',
         AdminServiceDeleteView.as_view(), name="adminservicedelete"),

# forservice package
path('med-admin/servicepackage/list/',
         AdminServicePackageListView.as_view(), name="adminservicepackagelist"),
path('med-admin/servicepackage/create/',
         AdminServicePackageCreateView.as_view(), name="adminservicepackagecreate"),
path('med-admin/<int:pk>/packageedit/',
         AdminServicePackageUpdateView.as_view(), name="adminservicepackageupdate"),
path('med-admin/<int:pk>/packagedelete/',
         AdminServicePackageDeleteView.as_view(), name="adminservicepackagedelete"),

# for team
path('med-admin/team/list/',
         AdminTeamListView.as_view(), name="adminteamlist"),
path('med-admin/team/create/',
         AdminTeamCreateView.as_view(), name="adminteamcreate"),
path('med-admin/<int:pk>/teamedit/',
         AdminTeamUpdateView.as_view(), name="adminteamupdate"),
path('med-admin/<int:pk>/teamdelete/',
         AdminTeamDeleteView.as_view(), name="adminteamdelete"),

# for offer
path('med-admin/offer/list/',
         AdminOfferListView.as_view(), name="adminofferlist"),
path('med-admin/offer/create/',
         AdminOfferCreateView.as_view(), name="adminoffercreate"),
path('med-admin/<int:pk>/offeredit/',
         AdminOfferUpdateView.as_view(), name="adminofferupdate"),
path('med-admin/<int:pk>/offerdelete/',
         AdminOfferDeleteView.as_view(), name="adminofferdelete"),

# for subscriber
path('med-admin/subscriber/list/',
         AdminSubscriberListView.as_view(), name="adminsubscriberlist"),
path('med-admin/subscriber/create/',
         AdminSubscriberCreateView.as_view(), name="adminsubscribercreate"),
path('med-admin/<int:pk>/subscriberedit/',
         AdminSubscriberUpdateView.as_view(), name="adminsubscriberupdate"),
path('med-admin/<int:pk>/subscriberdelete/',
         AdminSubscriberDeleteView.as_view(), name="adminsubscriberdelete"),

# for testimonial
path('med-admin/testimonial/list/',
         AdminTestimonialListView.as_view(), name="admintestimoniallist"),
    path('med-admin/testimonial/create/',
         AdminTestimonialCreateView.as_view(), name="admintestimonialcreate"),
    path('med-admin/<int:pk>/testimonialedit/',
         AdminTestimonialUpdateView.as_view(), name="admintestimonialupdate"),
    path('med-admin/<int:pk>testimonialdelete/',
         AdminTestimonialDeleteView.as_view(), name="admintestimonialdelete"),

# for album
path('med-admin/album/list/',
         AdminAlbumListView.as_view(), name="adminalbumlist"),
path('med-admin/album/create/',
         AdminAlbumCreateView.as_view(), name="adminalbumcreate"),
path('med-admin/<int:pk>/albumedit/',
         AdminAlbumUpdateView.as_view(), name="adminalbumupdate"),
path('med-admin/<int:pk>albumdelete/',
         AdminAlbumDeleteView.as_view(), name="adminalbumdelete"),       

         # for image

path('med-admin/image/list/',
         AdminImageListView.as_view(), name="adminimagelist"),
path('med-admin/image/create/',
         AdminImageCreateView.as_view(), name="adminimagecreate"),
path('med-admin/<int:pk>/imageedit/',
         AdminImageUpdateView.as_view(), name="adminimageupdate"),
path('med-admin/<int:pk>imagedelete/',
         AdminImageDeleteView.as_view(), name="adminimagedelete"), 

# for video
path('med-admin/video/list/',
         AdminVideoListView.as_view(), name="adminvideolist"),
path('med-admin/video/create/',
         AdminVideoCreateView.as_view(), name="adminvideocreate"),
path('med-admin/<int:pk>/videoedit/',
         AdminVideoUpdateView.as_view(), name="adminvideoupdate"),
path('med-admin/<int:pk>videodelete/',
         AdminVideoDeleteView.as_view(), name="adminvideodelete"),
# for enqury
path('med-admin/enquery/list/',
         AdminEnqueryListView.as_view(), name="adminenquerylist"),
path('med-admin/enquery/create/',
         AdminEnqueryCreateView.as_view(), name="adminenquerycreate"),
path('med-admin/<int:pk>/enqueryedit/',
         AdminEnqueryUpdateView.as_view(), name="adminenqueryupdate"),
path('med-admin/<int:pk>enquerydelete/',
         AdminEnqueryDeleteView.as_view(), name="adminenquerydelete"),

# formessage
path('med-admin/message/list/',
         AdminMessageListView.as_view(), name="adminmessagelist"),
path('med-admin/message/create/',
         AdminMessageCreateView.as_view(), name="adminmessagecreate"),
path('med-admin/<int:pk>/messageedit/',
         AdminMessageUpdateView.as_view(), name="adminmessageupdate"),
path('med-admin/<int:pk>messagedelete/',
         AdminMessageDeleteView.as_view(), name="adminmessagedelete"),
	]