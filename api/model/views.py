import cv2
import json
import base64
import os
from os import listdir
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from api.model.models import Model,Dataset,Disease
from api.authentication.views import decode_token,get_permission,is_supperuser
from ultralytics.models import YOLO
from core.settings import MODEL,DATASET
from rest_framework import status
from PIL import Image

# Create your views here.
@csrf_exempt
def get_request(request):
    token = request.COOKIES.get("token")
    if(token is None):
        return JsonResponse({"msg":"must be logged in"})
    res = decode_token(token=token)
    
    request.session.set_test_cookie()
    if request.method == 'POST': # and request.FILES.getlist('image'):
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        try:
                model_name = Model.objects.get(isActive=True)

        except:
            return JsonResponse({"msg":"model not found"})
        
        model = YOLO(MODEL / "{}".format(model_name.path))
        
        response = []

        for image in request.FILES.getlist('image'):
            # print("image",image)
            image_path = default_storage.save('tmp/' + image.name, image)
            image_full_path = default_storage.path(image_path)
            
            img = cv2.imread(image_full_path)
            results = model(img)
            
            for result in results:
                # print(result.summary())
                data = result.summary()[0]
                class_path = DATASET / "{}/val/{}".format(model_name.dataset.path,data["name"])
                # image_binary = base64.b64encode(load_image(class_path))
                
                image_binary = base64.b64encode(load_image(class_path).read())
                # img = load_image(class_path)
                # cv2.imshow("image",img)
                data["image_name"] = image.name
                data["image_base64"] = image_binary.decode('utf-8')
                # print(data)
                response.append(data)
                continue
                # return HttpResponse(result.tojson())
            
            # print("image",response)
        return JsonResponse(response,status = status.HTTP_200_OK,safe=False)
    return JsonResponse({"msg":"get request"})

def load_image(path):
    image_path = listdir(path)
    # print(image_path)
    return open(os.path.join(path,image_path[0]),'rb')
      
    # cv2.imshow(image_path[0],img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

@csrf_exempt
@require_http_methods(['POST'])
async def train_model(request):
    try:
        model_name = Model.objects.get(path = request.POST.get("model"))
        print(os.path.join(MODEL,model_name.path))
        model = YOLO(os.path.join(MODEL,model_name.path))
    except:
        return JsonResponse({"msg":"model not found"})
    
    dataset =Dataset.objects.get(path = request.POST.get("dataset"))
    data = os.path.join(DATASET,dataset.path)
    
    permission = get_permission(token=request.COOKIES.get("token"))
    if permission != "admin":
        return JsonResponse({"msg":"permission not allowed train model"})
   
    epoochs = request.POST.get("epochs")
    batch =  request.POST.get("batch")
    worker  = request.POST.get("worker")
    imgsz =  request.POST.get("imgsz")
    result = await model.train(task='classify',mode='train',data=data,epochs=epoochs,batch=batch,workers=worker,imgsz=imgsz)
    return JsonResponse({"result":result},safe=False)

@require_http_methods(["GET"])
def get_all_model(request):
    token = request.COOKIES.get("token")
    if token is None:
        return JsonResponse({"msg":"must be logged in"},status.HTTP_401_UNAUTHORIZED)
    
    permission = get_permission(token=token)
    if permission != 'admin':
        return JsonResponse({"msg":"permission not allowed"},status.HTTP_403_FORBIDDEN)
    
    try:
        model = list(Model.objects.all().values())
        return JsonResponse(model,safe=False)
    except:
        return JsonResponse({"msg":"model not found"},status.HTTP_404_NOT_FOUND)
    
@require_http_methods(["GET"])
def get_active_model(request):
    token = request.COOKIES.get("token")
    if token is None:
        return JsonResponse({"msg":"must be logged in"},status.HTTP_401_UNAUTHORIZED)
    
    permission = get_permission(token=token)
    if permission != 'admin':
        return JsonResponse({"msg":"permission not allowed"},status.HTTP_403_FORBIDDEN)
    
    try:
        model = list(Model.objects.filter(isActive=True).values())
        return JsonResponse(model[0],safe=False)
    except:
        return JsonResponse({"msg":"model not found"},status.HTTP_404_NOT_FOUND)

@require_http_methods(["GET"])
def get_all_dataset(request):
    token = request.COOKIES.get("token")
    if token is None:
        return JsonResponse({"msg":"must be logged in"},status.HTTP_401_UNAUTHORIZED)
    
    permission = get_permission(token=token)
    if permission != 'admin':
        return JsonResponse({"msg":"permission not allowed"},status.HTTP_403_FORBIDDEN)
    
    try:
        dataset = list(Dataset.objects.all().values())
        print(dataset)
        return JsonResponse(dataset,status=status.HTTP_200_OK,safe=False)
    except:
        return JsonResponse({"msg":"dataset not found"},status.HTTP_404_NOT_FOUND)

@require_http_methods(["GET"])
def get_all_diseases(request):
    try:
        di = list(Disease.objects.all().values())
        
        return JsonResponse(di,status=status.HTTP_200_OK,safe=False)
    except:
        return JsonResponse({"msg":"disease not found"},status.HTTP_404_NOT_FOUND)

@require_http_methods(["POST"])
@csrf_exempt
def create_new_disease(request):
    if not is_supperuser(request=request):
        return JsonResponse({"msg":"permission not allowed"},status.HTTP_403_FORBIDDEN)
    
    name = request.POST.get("name")
    description = request.POST.get("description")
    type = request.POST.get("type")

    try:
        disease = Disease.objects.create(name=name,description=description,type=type)
        print(disease)
        return JsonResponse({"msg":"create new disease successfull"},status = status.HTTP_201_CREATED,safe=False)
    except:
        return JsonResponse({"msg":"Cannot create new disease"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@require_http_methods(['POST'])
@csrf_exempt
def update_disease(request,id):
    if not is_supperuser(request=request):
        return JsonResponse({"msg":"permission not allowed"},status.HTTP_403_FORBIDDEN)
    name = request.POST.get("name")
    description = request.POST.get("description")
    type = request.POST.get("type")
    print(id)
    try:
        disease = Disease.objects.get(id=id)
    except:
        return JsonResponse({"msg":"disease with id not found"},status=status.HTTP_404_NOT_FOUND)
    
    try:
        disease.name = name
        disease.description = description
        disease.type = type
        disease.save()
    except Exception as e:
        print(e)
        return JsonResponse({"msg":"update disease error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse({"id":id},status = status.HTTP_200_OK,safe=False)

@csrf_exempt    
def get_disease(request,id):
    
    return JsonResponse({"id":id})