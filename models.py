
from django.db import models



class Doctor(models.Model):
    did=models.AutoField(primary_key=True,unique=True)
    age = models.IntegerField()
    name=models.CharField(max_length=50)
    special = models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    experience=models.IntegerField()
    email = models.EmailField(default='default@example.com')

   
    def __str__(self):
        return self.name

class Patient(models.Model):
    
    pid=models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    age=models.IntegerField()
    mobile=models.IntegerField()
    address=models.CharField(max_length=150)

    

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.CharField(default='hari',max_length=50)
    ChildName=models.CharField(default='hari',max_length=50)
    ChildAge=models.IntegerField(default=23)
    symptoms=models.CharField(default='cold',max_length=50)
    Mobilenumber=models.CharField(default='9652636552',max_length=50)
    Address=models.CharField(default='vizag',max_length=250)
    visited = models.BooleanField(default=False)


    def __str__(self):
        return self.ChildName
    
class Child(models.Model):
    
    name=models.CharField(max_length=50)
    date=models.DateField()    
    blood=models.CharField(max_length=50)
    parent=models.CharField(max_length=50)
    age=models.CharField(default='1 year 4months',max_length=250)
 

    def __str__(self):
        return self.name

class review(models.Model):
    pname=models.CharField(max_length=50)
    dname=models.CharField(max_length=50)
    comments=models.CharField(max_length=150)

    def __str__(self):
        return self.pname
class vnc(models.Model):
    vname=models.CharField(max_length=100)
    vdiscript=models.CharField(max_length=150)
    vdate=models.CharField(max_length=50)

    def __str__(self) :
        return self.vdate
    

    




    

