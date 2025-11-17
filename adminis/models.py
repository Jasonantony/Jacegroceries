from django.db import models


class Landlord(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    store_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    established_date = models.DateField()  
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name


class VendorRegistration(models.Model):
    vendor_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    registered_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.vendor_name


class HiringRequest(models.Model):
    applicant_name = models.CharField(max_length=100)
    position_applied = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.applicant_name


class Firing(models.Model):
    employee_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    terminated_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return self.employee_name
