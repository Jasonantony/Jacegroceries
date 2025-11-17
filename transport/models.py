from django.db import models

class vechile_register(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class vechicle_assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    vehicle = models.ForeignKey(vechile_register, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    assignment_date = models.DateField(auto_now_add=True)
    pickup_point = models.CharField(max_length=200)
    drop_point = models.CharField(max_length=200)
    total_stock = models.IntegerField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vehicle_number} - {self.driver_name}"