from asyncore import read
import pickle
from tempfile import tempdir
from flask import Flask, render_template, redirect, request, url_for
import numpy as np
file = open("grade_model.pkl",'rb')
model = pickle.load(file)

app = Flask(__name__)
app.config['SECRET_KEY'] = "Yashnegi@01"
sex_M = 0
school_MS =0
Pstatus_T = 0
famsize_LE3 = 0
address_U = 0
Fedu = 0
Mjob_health, Mjob_other, Mjob_services, Mjob_teacher = 0, 0, 0, 0
Fjob_health, Fjob_other, Fjob_services, Fjob_teacher = 0, 0, 0, 0
Medu = 0
reason_home, reason_other, reason_reputation = 0, 0, 0
guardian_mother, guardian_other = 0, 0
traveltime, studytime = 0, 0
schoolsup_yes, famsup_yes = 0, 0
paid_yes, activities_yes, nursery_yes, higher_yes, internet_yes, romantic_yes = 0, 0, 0, 0, 0, 0
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        global temp
        global g2 
        global temp
        
        age= int(request.form.get("Age"))
        gender = request.form.get("gender")
        if gender == "Male":
            sex_M =1
        else:
            sex_M=0
        
        ownership = request.form.get("schoolOwnership")
        if ownership == "Public":
            school_MS = 1
        else:
            school_MS = 0
        
        pstatus = request.form.get("q21_parentsLiving")
        if pstatus == "Yes":
            Pstatus_T = 1
        else :
            Pstatus_T = 0
        
        famsize = request.form.get("q20_familySize")
        if famsize=="1" or famsize=="2" or famsize=="3":
            famsize_LE3 =1
        elif famsize == "Greater than 3" :
            famsize_LE3=0
            
        area = request.form.get("q48_area")
        if area == "Urban":
            address_U = 1
        else :
            address_U =0
        
        
        mjob = request.form.get("q24_mothersJob")
        if mjob =="Health Worker":
            Mjob_health = 1
            Mjob_other, Mjob_services, Mjob_teacher = 0, 0, 0
        elif mjob == "Teacher":
            Mjob_teacher =1
            Mjob_health, Mjob_other, Mjob_services = 0, 0, 0
        elif mjob == "Civil Services":
            Mjob_services =1
            Mjob_health, Mjob_other, Mjob_teacher = 0, 0, 0
        elif mjob == "Other" :
            Mjob_other =1
            Mjob_health, Mjob_services, Mjob_teacher = 0, 0, 0
        else :
            Mjob_health, Mjob_other, Mjob_services, Mjob_teacher = 0, 0, 0, 0            
        
        fjob = request.form.get("q25_typeA25")
        if fjob =="Health Worker":
            Fjob_health = 1
            Fjob_other, Fjob_services, Fjob_teacher = 0, 0, 0
        elif fjob == "Teacher":
            Fjob_teacher =1
            Fjob_health, Fjob_other, Fjob_services = 0, 0, 0
        elif fjob == "Civil Services":
            Fjob_services =1
            Fjob_health, Fjob_other, Fjob_teacher = 0, 0, 0
        elif fjob == "Other" :
            Mjob_other =1
            Fjob_health, Fjob_services, Fjob_teacher = 0, 0, 0
        else :
            Fjob_health, Fjob_other, Fjob_services, Fjob_teacher = 0, 0, 0, 0 
        
        faed = request.form.get("q23_fathersEducation")
        if faed == "None":
            Fedu = 0
        elif faed == "Primary education(4th grade)":
            Fedu = 1
        elif faed == "5th to 9th grade":
            Fedu = 2
        elif faed == "Secondary education":
            Fedu = 3
        else :
            Fedu = 4    
        moed = request.form.get("q22_mothersEducation")
        if moed == "None":
            Medu = 0
        elif moed == "Primary education(4th grade)":
            Medu = 1
        elif moed == "5th to 9th grade":
            Medu = 2
        elif moed == "Secondary education":
            Medu = 3
        else :
             Medu = 4 
        reason = request.form.get("q26_reasonFor")
        if reason == "Close to home":
          reason_home =1
          reason_other, reason_reputation = 0, 0
        elif reason == "Reputation of School":
              reason_reputation= 1
              reason_home, reason_other = 0, 0
        elif reason == "Other":
            reason_other =1
            reason_home, reason_reputation = 0, 0
        else :
             reason_home, reason_other, reason_reputation = 0, 0, 0
        guardian = request.form.get("q28_whoIs")
        if guardian == "Mother":
            guardian_mother, guardian_other = 1, 0
        elif guardian == "Other":
            guardian_mother, guardian_other = 0, 1
        else :
            guardian_mother, guardian_other = 0, 0
        
        traveltime1 = int(request.form.get("q29_travelTimein"))
        if traveltime1<15:
            traveltime = 1
        elif traveltime1>=15 and traveltime1<30:
            traveltime = 2
        elif traveltime1>=30 and traveltime1<60:
            traveltime = 3
        else:
            traveltime = 4
        
        studytime1 = int(request.form.get("q30_studyTimein"))
        if studytime1<2:
            studytime = 1
        elif studytime1>=2 and traveltime1<5:
            studytime = 2
        elif studytime1>=5 and traveltime1<10:
            studytime = 3
        else:
            studytime = 4
            
        failures = request.form.get("q31_numberOf")
        support = request.form.get("q32_extraSupport")
        if support == "Yes":
            schoolsup_yes = 1
        else:
            schoolsup_yes =0
        famsupport = request.form.get("q33_educationalSupport")
        if famsupport == "Yes":
            famsup_yes = 1
        else:
            famsup_yes =0
        
        extraclasses = request.form.get("q34_extraPaid")
        if extraclasses == "Yes":
            paid_yes = 1
        else:
            paid_yes =0
            
        curactivities = request.form.get("q35_extracurricularActivities")
        if curactivities == "Yes":
            activities_yes = 1
        else:
            activities_yes = 0
            
        nursery = request.form.get("q36_haveYou")
        if nursery == "Yes":
            nursery_yes = 1
        else:
            nursery_yes = 0
        
        highed = request.form.get("q37_doYou")
        if highed == "Yes":
            higher_yes = 1
        else :
            higher_yes = 0
            
        rompart = request.form.get("q39_doYou39")
        if rompart == "Yes":
            romantic_yes = 1
        else:
            romantic_yes = 0
        internet = request.form.get("q38_internetAccess")
        if internet == "Yes":
            internet_yes =1
        else :
            internet_yes=0
        famrel = request.form.get("q40_qualityOf")
        goout = request.form.get("q41_goingOut")
        Dalc = request.form.get("q42_number42")
        Walc = request.form.get("q43_weekendAlcohol")
        health = request.form.get("q44_number44")
        absences = request.form.get("q45_number45")
        g1 = request.form.get("q46_enterG1first")
        freetime = request.form.get("q49_number")        
        g2= request.form.get("q47_number47")
        global g3
        g3 = model.predict([[age, Medu, Fedu, traveltime, studytime, failures, famrel,
       freetime, goout, Dalc, Walc, health, absences, 
       school_MS, sex_M, address_U, famsize_LE3, Pstatus_T,
       Mjob_health, Mjob_other, Mjob_services, Mjob_teacher,
       Fjob_health, Fjob_other, Fjob_services, Fjob_teacher,
       reason_home, reason_other, reason_reputation, guardian_mother,
       guardian_other, schoolsup_yes, famsup_yes, paid_yes,
       activities_yes, nursery_yes, higher_yes, internet_yes,
       romantic_yes,g1, g2]])
        
        return redirect("/result")
       
    return render_template("home.html")

@app.route("/result", methods=["GET", "POST"])
def res():
    if g3[0]>15:
        remark = "Good work, keep it up"
    elif g3[0]>=10 and g3[0]<=15:
        remark ="Work Harder To acheive top grade"
    else:
        remark = "Lot of practice and hardwork required, concentrate on studies more!"
    return render_template("result.html", temp =round(g3[0]), remark=remark)
    
if __name__ == "__main__":
    app.run(debug=True)