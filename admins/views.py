from django.shortcuts import render,HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from users.models import UserRegistrationModel
from .modelsexe.StartProcess import MyModelStartExecution
import subprocess
# Create your views here.

def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')
        elif usrid == 'Admin' and pswd == 'Admin':
            return render(request, 'admins/AdminHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def ViewRegisteredUsers(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/RegisteredUsers.html', {'data': data})


def AdminActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/RegisteredUsers.html', {'data': data})

def TestCTScanImageForm(request):
    return render(request,"admins/CTScanImageUpload.html",{})

# def UploadImageAction(request):
#     image_file = request.FILES['file']
#     # let's check if it is a csv file
#     if not image_file.name.endswith('.png'):
#         messages.error(request, 'THIS IS NOT A PNG  FILE')


#     fs = FileSystemStorage(location="media/ctscans/")
#     filename = fs.save(image_file.name, image_file)
#     # detect_filename = fs.save(image_file.name, image_file)
#     uploaded_file_url = "/media/ctscans/" + filename  # fs.url(filename)
#     print("Image path ", uploaded_file_url)
#     prog = 'python PredictionCTScamImages/predict_ct_scan.py '+uploaded_file_url+' '
#     #subprocess.call(prog)
#     result = "COvid"

#     obj = MyModelStartExecution()
#     result = obj.startProcess(uploaded_file_url)
#     print("Result=",result)

#     return render(request,"admins/CTScanImageUpload.html",{'result':result})

def UploadImageAction(request):
    try:
        image_file = request.FILES['file']

        # Check if the uploaded image is empty
        if image_file.size == 0:
            messages.error(request, 'Uploaded image is empty.')
            return render(request, "admins/CTScanImageUpload.html", {'result': 'Covid-19'})

        # Check if the file extension is a supported image format
        if not image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            messages.error(request, 'This is not a supported image file.')
            return render(request, "admins/CTScanImageUpload.html", {'result': 'Covid-19'})

        # Validate the image file format using PIL
        try:
            Image.open(image_file)
        except ValidationError:
            messages.error(request, 'Uploaded file is not a valid image.')
            return render(request, "admins/CTScanImageUpload.html", {'result': 'Covid-19'})

        # Continue with the file upload and processing
        fs = FileSystemStorage(location="media/ctscans/")
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = "/media/ctscans/" + filename

        print("Image path ", uploaded_file_url)

        prog = 'python PredictionCTScamImages/predict_ct_scan.py ' + uploaded_file_url + ' '
        # subprocess.call(prog)

        obj = MyModelStartExecution()
        result = obj.startProcess(uploaded_file_url)
        print("Result=", result)

        return render(request, "admins/CTScanImageUpload.html", {'result': result})

    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return render(request, "admins/CTScanImageUpload.html", {'result': 'Covid-19'})