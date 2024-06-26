from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.verify import authentication, form_varification
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from datetime import datetime
from .form import signature_form
from .models import Verify_sign
from .process import extract_sign
import os
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image
# Create your views here.

loaded_model = load_model('dataset/binary_classification_model.h5')

def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html")

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    # return HttpResponse("This is Home page")    
    return render(request, "log_in.html")

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(fname, contact_no, ussername)
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
    # return HttpResponse("This is Home page")    
    return render(request, "register.html")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'fname': request.user.first_name,
        }
    
    return render(request, "dashboard.html",context)



@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def sign_verify(request):
    context = {
        'fname': request.user.first_name,
        }
    if request.method == "POST":
        pname = request.POST['pname']
        uploaded_doc = request.FILES['uploaded_doc']
        s = Verify_sign(pname=pname,uploaded_doc=uploaded_doc)
        s.save()

        # Define the image dimensions and number of classes
        img_width, img_height = 224, 224

        uploaded_image = Image.open(uploaded_doc.file)
        img = uploaded_image.resize((img_width, img_height))
        # Convert the image to grayscale
        img_gray = img.convert("L")

        # Invert the grayscale image (convert white to black and vice versa)
        img_inverted = Image.eval(img_gray, lambda x: 255 - x)

        # Convert the grayscale image to an array
        img_array = image.img_to_array(img_inverted)

        # Duplicate the single channel to create three channels (RGB)
        img_rgb = np.repeat(img_array, 3, axis=-1)

        # Reshape the image to match the model's input shape
        img_rgb = np.expand_dims(img_rgb, axis=0)
        img_rgb /= 255.  # Normalize the pixel values
        # Use your model to predict the class of the uploaded image
        pred = loaded_model.predict(img_rgb)
        
        confidence = pred if pred > 0.5 else 1 - pred
        print("Confidence level:", confidence, type(confidence))
        
        # pred = round(pred[0][0], 2)
        print(pred)
        if pred > 0.5 and pred <= 1:
            class_label = "onkar_sign"
        elif pred <= 0.5 and pred >= 0 and confidence >= 0.9:
            class_label = "aniket_sign"
        else:
            class_label = "not_found"
        # Determine the predicted class based on the probability score
        
        print("Predicted class:", class_label)
      
        verify_data = Verify_sign.objects.last()
        if class_label == pname:
            context = {
                'fname': request.user.first_name,
                'verify_data' : verify_data,
                'Identified' : "Signature_Identified"
                
                }
            return render(request, "results.html",context)
        else:
            context = {
                
                'verify_data' : verify_data,
                'Not_Identified' : "forged/Signature Not Identified"
                }
            return render(request, "results.html",context)
   
    return render(request,"sign_verify.html", context)




@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def results(request):
    context = {
        'fname': request.user.first_name,
        }
    
    return render(request, "results.html",context)