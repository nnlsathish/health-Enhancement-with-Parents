from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
from django.shortcuts import render
from datetime import datetime
from healthgoapp.models import *
from .forms import AppointmentForm


import mysql.connector as sql
#login for both 
dem=''
d=''
pwd=''
pn=''
pp=''

# appointment
cn = ''
ca = ''
sy = ''
mn = ''
lo = ''
do=''

# parent


pn = ''
pa = ''
pp = ''
pad = ''

# doctor

dem=''
dna = ''
dag = ''
ds = ''
dl = ''
dex = ''

#vaccine

vna=''
vds=''
vda=''

#child
cpna=''
cn=''
cdb=''
cb=''

#feedback
pna=''
dnam=''
com=''

def index(request):
    return render(request, 'index.html')
#doctor signup page
def signup(request):
    error=""
    global dna, dag, ds, dl, dex
    
    if request.method=='POST':
        n=request.POST['dage']
        c=request.POST['dname']
        p=request.POST['dsp']
        sp=request.POST['daddress']
        e=request.POST['dexp']
        em=request.POST['email']

        try:
            Doctor.objects.create(age=n,name=c,special=p,address=sp,experience=e,email=em)

            error="No"

        except:
            error="Yes"
        
        m =sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():

            if key == "dage":
                dag = value
            if key == "dname":
                dna = value 
            if key == "dsp":
                ds = value
            if key == "daddress":
                dl = value
            if key == "dexp":
                dex = value
            if key == "email":
                dem = value       

        c = "insert into doctors (doctor_age,doctor_name,specialist,location,experience,email) values('{}','{}','{}','{}','{}','{}')".format(
            dag, dna, ds, dl, dex,dem)
        cursor.execute(c)
        m.commit()
    d={'error':error}    
    return render(request, 'signup_page.html',d)
#parent signup page
def psignup(request):
        error=""
        global pn, pa, pp, pad
        if request.method=='POST':
            n=request.POST['name']
            g=request.POST['age']
            m1=request.POST['phone']
            a1=request.POST['address']


            try:
               Patient.objects.create(name=n,mobile=m1,age=g,address=a1)

               error="No"

            except:
               error="Yes"
            m = sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
            cursor = m.cursor()
            d = request.POST
            for key, value in d.items():

                if key == 'name':
                    pn = value
                if key == 'age':
                    pa = value
                if key == 'phone':
                    pp = value
                if key == 'address':
                    pad = value
            c = "insert into parents ( parient_name,parient_age,phone,parent_location ) values('{}','{}','{}','{}')".format(
                pn, pa, pp, pad)
            cursor.execute(c)
            m.commit()
        d={'error':error}     
        return render(request, 'patientsignup.html')
#doctor login 

def loginaction(request):
    global dem,pwd
    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="password":
                pwd=value
            if key=="email":
                dem=value    
        c="select * from doctors where    doctor_name='{}' and Email='{}'".format(pwd,dem)
        cursor.execute(c)
        t=tuple(cursor.fetchall())   
        if t==():
            return render(request,'error.html')    
        else:
            # session - store doctor id / name
            request.session["usertype"]="doctor"
            request.session["userid"]=t[0]
            request.session['username']=pwd
            print(pwd)
            return render(request,'doctor.html', {'data':dem})
    return render(request,'login_page.html')

#patient login
def plogin(request):
    global pn,pp
    if request.method == 'POST':
        m = sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "name":
                pn = value
            if key == "password":
                pp = value
        c = "select * from parents where parient_name='{}' and phone='{}'".format(pn,pp)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        if t == ():
            return render(request, 'error.html')
        else:
            request.session["usertype"]="patient"
            request.session["userid"]=t[0]

            request.session['username']=pn
            print(pn)
            return render(request, 'patient.html', {'data':pn})
    return render(request, 'plogin.html')

#Diet

def diet(request):
    return render(request,'diet.html')

#Vacction chart
def vacction(request):
    # fetch children details
    m = sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
    cursor = m.cursor()
    pn = request.session['username']
    c = "select *,datediff(curdate(),date(dbirth)) from child where parentname='{}' ".format(pn)
    cursor.execute(c)
    t = tuple(cursor.fetchall())
    results={}
    if t == ():
        return render(request, 'error.html')
    else:
        for ch in t:
            # subtract child dob from system date
            days = ch[-1]
            months= days/30
            details='-'
            if months>0 and months<=2:
                details='DTaP, Hib, IPV, PCV, RV'
            if months>2 and months<=4:
                details='DTaP, Hib, IPV, PCV, RV'
            if months>4 and months<=6:
                details='DTaP, Hib, IPV, PCV, RV'
            if months>12 and months<=15:
                details='MMR (Measles, Mumps, Rubella), Varicella (Chickenpox), PCV, Hib'
            if months>15 :
                details='DTaP, IPV'
            results[ch]=details
            # switch - case   0 to 3 => list of vaccines

        return render(request, 'vaccination.html', {'data':results})

    return render(request,'vaccination.html')

# Appointment

def appointment(request):
        error=""
        doctor1 = Doctor.objects.all()
        global cn,ca,sy,mn,lo,do
        if request.method == 'POST':
            d=request.POST['doctor'] +"-"+str(request.session["userid"][0])
            cn=request.POST['cn']+"-"+str(request.session["userid"][0])
            ca=request.POST['ca']
            sy=request.POST['ms']
            mn=request.POST['mn']
            lo=request.POST['ad']
            doctor=Doctor.objects.filter(name=d).first()
            print(d)
        

            try:
                Appointment.objects.create(ChildName=cn,ChildAge=ca,symptoms=sy,Mobilenumber=mn,Address=lo,doctor=d)

                error="No"

            except:
                error="Yes"
            
            m = sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
            cursor = m.cursor()
            d = request.POST
            for key, value in d.items():

                if key == "cn":
                    cn = value
                if key == "ca":
                    ca = value
                if key == "ms":
                    sy = value
                if key == "mn":
                    mn = value
                if key == "ad":
                    lo = value
                if key == "doctor":
                    do = value    

            c = "insert into appointments (child_name,child_age,syntoms,phone,location,doctor) values('{}','{}','{}','{}','{}','{}')".format(cn,ca,sy,mn,lo,do)
            cursor.execute(c)
            m.commit()
        d={'error':error,'doctor':doctor1}    
        return render(request, 'appointment.html',d)

#vaccine

def vaccine(request):
    error=""
    global vna,vds,vda
    if request.method == 'POST':
        d=request.POST['vn']
        cn=request.POST['vd']
        ca=request.POST['sd']
        
        try:
                vnc.objects.create(vdiscript=cn,vdate=ca,vname=d)

                error="No"

        except:
            error="Yes"
       

        m = sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():

            if key == "vn":
                vna = value
            if key == "vd":
                vds = value
            if key == "sd":
                vda = value
            

        c = "insert into  vaccine (vaccine_name,vaccine_description,schedule_time) values('{}','{}','{}')".format(vna,vds,vda)
        cursor.execute(c)
        m.commit()
    d={'error':error}    
    return render(request, 'vaccine.html',d)

#View_doctors

def view_Doctor(request):
    #query = request.GET.get('q')
    #print(query)
    #doc = Doctor.objects.values(special=query)
    doc=Doctor.objects.all()
    d={'doc':doc}
    return render(request,'view_doctor.html',d)
#delete doctor

from textblob import TextBlob

def analyze_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    
    # Get the sentiment polarity
    sentiment_score = blob.sentiment.polarity
    
    # Define sentiment categories based on polarity score
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

def view_DoctorQ(request):
    query = request.GET.get('q')
    print(query)
    reviews = review.objects.all().values() # filter(dname=d['name']).values()
    print('r count', len(reviews))
    doc = Doctor.objects.filter(special=query).values()
    print('doc count', len(doc))
    #doc=Doctor.objects.all()
    #feedback table - get data - train with naivebayes - get rank
    #order based on reviews - naivebayes
    poslist=[]
    pos=0
    #neg=0
    for d in doc:
        print('name--','..',d['name'])
        reviews = review.objects.filter(dname=d['name']).values()
        pos=0
        #print('count', len(reviews))        
        for r in reviews:
            text = r['comments']
            print('r is ', r['comments'])
            sentiment = analyze_sentiment(text)
            print(text, '-', sentiment )
            #print("Sentiment:",sentiment)
            if sentiment=="Positive":
                pos+=1
        poslist.append(pos)
    r=range(len(doc))
    # for x in r:    
    #     print('--',x)
    i=0
    for x in doc:
        x['pos']=poslist[i]
        i+=1
    d={'doc':doc, 'count':r}
    return render(request,'view_doctorQ.html',d)

def Delete_Doctor(request,pid):
    doctor= Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

#view_patient

def view_Patient(request):
    pat=Patient.objects.all()
    d={'pat':pat}
    return render(request,'view_patient.html',d)

#delete_patient

def Delete_Patient(request,pid):
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

#add_Child
def child(request):
    error=""
    global cpna,cn,cdb,cb
    if request.method == 'POST':
        cn=request.POST['child1-name']
        ca=request.POST['child1-dob']
        start_date=ca
        current_date = datetime.now()
        date1 = datetime.strptime(start_date, "%Y-%m-%d")
        date2 = datetime.strptime(str(current_date), "%Y-%m-%d %H:%M:%S.%f")
        diff = relativedelta(date2, date1)

        # Get the years and months
        years = diff.years
        months = diff.months
        
        print(f"{years} years and {months} months")

        #diff=start_date-current_date
        #years = diff.days // 365
        #months = (diff.days % 365) // 30
        age= f"{years} years {months} months"
      
        sy=request.POST['child1-blood-group']
        cp=request.POST['Parent']
       

        try:
            Child.objects.create(name=cn,date=ca,blood=sy,parent=cp,age=age)

            error="No"

        except:
            error="Yes"
            
        m = sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
        
            if key == "child1-name":
                cn = value
            if key == "child1-dob":
                cdb = value
            if key == "child1-blood-group":
                cb = value
            if key == "Parent":
                cpna = value    
               
           
        c = "insert into  child (child_name,dbirth ,blood_group,parentname) values('{}','{}','{}','{}')".format(cn,cdb,cb,cpna)
        cursor.execute(c)
        m.commit()
    d={'error':error}    
    return render(request,'add_child.html',d)

#feedback
def feedback(request):
    error=""
    global pna,dnam,com
    if request.method == 'POST':
        cn=request.POST['patient-name']
        ca=request.POST['doctor-name']
        sy=request.POST['comments']
        try:
            review.objects.create(pname=cn,dname=ca,comment=sy)

            error="No"

        except:
            error="Yes"
            


        m = sql.connect(host="localhost",user="root",passwd="Sathish@2003",database="healthcare")
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():

            if key == "patient-name":
                pna = value
            if key == "doctor-name":
                dnam = value
            if key == "comments":
                com = value
            

        c = "insert into  feedback ( pname,dname,comments ) values('{}','{}','{}')".format(pna,dnam,com)
        cursor.execute(c)
        m.commit()
    d={'error':error}
    return render(request,'feedback.html',{"dname":request.GET.get('dname')})
# viwe_appintments

def view_appointmentQ(request):
    query = request.GET.get('q')
    print(query)
    doc = Appointment.objects.filter(symptoms=query).values()
    #doc=Doctor.objects.all()
    #feedback table - get data - train with naivebayes - get rank
    #order based on reviews - naivebayes
    d={'doc':doc}
    return render(request,'view_appointmentQ.html',d)

def view_appoint(request):
    Email = request.session['username']
    print(Email)
    ut=request.session["usertype"]
    #doc_name=Doctor.objects.filter(email__contains=request.session['username'][0])
    #print(doc_name)
    #print("demo",ut)
    if ut=='doctor':
       
        doc=Appointment.objects.filter(doctor__contains=str(request.session["username"]))
    elif ut=='patient':
        print(request.session["userid"][0])
        doc=Appointment.objects.filter(ChildName__contains=str(request.session["userid"][0]))
        pass 
    #doc=Appointment.objects.all()

    d={'doc':doc}
    return render(request,'view_appointment.html',d)
def vappoint(request):
    doc=Appointment.objects.all()
    d={'doc':doc}
    return render(request,'view_appointment.html',d)



# delete_appintments
def Delete_appoint(request,pid):
    patient = Appointment.objects.get(id=pid)
    patient.delete()
    return redirect('view_appointment')
#view_child
def view_child(request):
    
    doc=Child.objects.filter(parent__contains=str(request.session["username"]))
    d={'doc':doc}
    return render(request,'view_child.html',d)
# delete_child
def Delete_child(request,pid):
    patient = Child.objects.get(id=pid)
    patient.delete()
    return redirect('view_child')
# view_vaccine
def view_vaccine(request):
    
    doc=vnc.objects.all()
    d={'doc':doc}
    return render(request,'view_vaccine.html',d)
# delete_vaccine
def Delete_vaccine(request,pid):
    patient = vnc.objects.get(id=pid)
    patient.delete()
    return redirect('view_vaccine')

#appointment_list
def appointment_list(request):
    appointments = Appointment.objects.filter(doctor__contains=str(request.session["username"]))
   
    return render(request, 'appointment_list.html', {'appointments': appointments})
#mark_appointment
def mark_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    #appointment = Appointment.objects.filter(doctor__contains=str(request.session["username"]))
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'mark_appointment.html', {'form': form})
#edit functions
def edit_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    if request.method == 'POST':
        child.name = request.POST.get('child1-name')
        child.date = request.POST.get('child1-dob')
        child.blood = request.POST.get('child1-blood-group')
        child.parent = request.POST.get('Parent')
        child.save()
        
        return redirect('view_child')
    
    return render(request, 'edit_patient.html', {'child': child})





