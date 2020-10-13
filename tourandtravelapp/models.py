from django.contrib.auth.models import User
from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Organization(TimeStamp):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logo")
    email = models.EmailField()
    phone = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    slogan = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField()
    mission_and_vision = models.TextField()
    profile_image = models.ImageField(upload_to="profile")
    website = models.CharField(max_length=200)
    map_location = models.CharField(max_length=200)
    favicon = models.ImageField(upload_to="favicon", null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    customer_served = models.ImageField(
        upload_to="customer_served", null=True, blank=True)
    awards = models.ImageField(upload_to="awards", null=True, blank=True)
    estb_date = models.DateField()

    def __str__(self):
        return self.name


class Service(TimeStamp):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    images = models.ImageField(upload_to="images")
    icon = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.title


class ServicePackage(TimeStamp):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=19, decimal_places=2)
    duration = models.PositiveIntegerField()
    details = models.TextField()
    image = models.ImageField(upload_to="image")

    def __str__(self):
        return self.title


class Booking(TimeStamp):
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200)
    date = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    kids = models.PositiveIntegerField(default=0)
    message = models.TextField()

    def __str__(self):
        return self.name + "(" + self.package.title + ")"


class Comment(TimeStamp):
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return self.name + "(" + self.package.title + ")"


class Offer(TimeStamp):
    title = models.CharField(max_length=200)
    offer_starts = models.DateField()
    offer_ends = models.DateField()
    packages = models.ManyToManyField(ServicePackage)
    details = models.TextField()
    cost = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.ImageField(upload_to="offerimage")

    def __str__(self):
        return self.title


class Team(TimeStamp):
    name = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    image = models.ImageField(upload_to="image")
    mobile = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    detail = models.TextField()

    def __str__(self):
        return self.name


class Subscriber(TimeStamp):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Testimonial(TimeStamp):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="photo")
    sayings = models.TextField()
    profession = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Album(TimeStamp):
    title = models.CharField(max_length=200)
    details = models.TextField()

    def __str__(self):
        return self.title


class Image(TimeStamp):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.caption


class Video(TimeStamp):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.title


class Enquery(TimeStamp):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=200)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    package = models.ForeignKey(
        ServicePackage, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class Message(TimeStamp):
    sender = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.sender
