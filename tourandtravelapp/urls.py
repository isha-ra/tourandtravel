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


	]