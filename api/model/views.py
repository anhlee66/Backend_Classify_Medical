import cv2
import json
import base64
import os
import torch 

from os import listdir
from django.shortcuts import render
from urllib.parse import parse_qs
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from api.model.models import Model,Dataset,Disease,Request
from api.authentication.views import (
    decode_token,
    get_permission,
    is_supperuser,
    is_logged_in)
from api.user.models import User
from ultralytics.models import YOLO
from core.settings import MODEL,DATASET
from rest_framework import status
from PIL import Image
from torchvision import transforms
from pytorch_msssim import ssim


# Create your views here.
@csrf_exempt
def get_request(request):
    token = request.COOKIES.get("token")
    if(token is None):
        return JsonResponse({"msg":"must be logged in"})
    cookie = decode_token(token=token)

    request.session.set_test_cookie()
    if request.method == 'POST': # and request.FILES.getlist('image'):
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        try:
                model_name = Model.objects.get(isActive=True)

        except:
            return JsonResponse({"msg":"model not found","error":True},status=status.HTTP_404_NOT_FOUND)
        
        model = YOLO(MODEL / "{}".format(model_name.path))
        
        response = []

        for image in request.FILES.getlist('image'):
            # print("image",image)
            image_path = default_storage.save('tmp/' + image.name, image)
            image_full_path = default_storage.path(image_path)
            
            img = cv2.imread(image_full_path)
            results = model(img)

            user = User.objects.get(id=cookie["id"])
            request = Request.objects.create(user=user,content="this is my request",image=image_path)
            print(request)
            result = results[0]
                # print(result.summary())
            datas = result.summary()
            
            for data in datas:
                # if data['confidence'] < 0.5:
                #     continue
                dir_compare = os.path.join(DATASET,"{}\\val\\{}".format(model_name.dataset.path,data["name"]))

                image_compare_list = get_similar_image(image_path=image_full_path,dir_compare=dir_compare,end=5)
                # print(len(image_compare_list))
                # class_path = DATASET / "{}/val/{}".format(model_name.dataset.path,data["name"])
                # image_binary = base64.b64encode(load_image(class_path))
                # print(image_compare)
                image_binary_list = []
                for image_compare in image_compare_list:
                    image_read = open(image_compare['path'],'rb').read()
                    image_binary = base64.b64encode(image_read)
                    image_binary_list.append({'image':image_binary.decode('utf-8')})
                data["image_name"] = image.name
                data["image_base64"] = image_binary_list
                print(data['confidence'])
                response.append(data)
                print(f"name: {data['name']} - confidence: {data['confidence']}")
                # return HttpResponse(result.tojson())
            
            print("image",response)
        if len(response) == 0 :
            return JsonResponse({"error":True},status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(response,status = status.HTTP_200_OK,safe=False)
    return JsonResponse({"msg":"get request"})

def load_image(path):
    image_path = listdir(path)
    # print(image_path)
    return open(os.path.join(path,image_path[0]),'rb')
      
    # cv2.imshow(image_path[0],img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def get_similar_image(image_path, dir_compare, start=0,end=1):
    image = Image.open(image_path)
    try:
        image_list = listdir(dir_compare)
    except:
        print(dir_compare)

    max = 0
    if end > len(image_list): 
        end = len(image_list)
    similar_image = []

    for img in image_list:
        img_compare = Image.open(os.path.join(dir_compare,img))

        # Define a transform to resize and convert to tensor
        transform = transforms.Compose([
            transforms.Resize((224,224)),  # Resize to the same size
            transforms.ToTensor(),  # Convert to tensor
        ])

        # Apply the transform
        tensor1 = transform(image)
        tensor2 = transform(img_compare)

        # Calculate Mean Squared Error
        mse = torch.mean((tensor1 - tensor2) ** 2)
        # print(f'Mean Squared Error: {mse.item()}')

        # Calculate SSIM
        ssim_index = ssim(tensor1.unsqueeze(0), tensor2.unsqueeze(0), data_range=1.0, size_average=True)
        # if max < ssim_index.item():
        #     max = ssim_index.item()
        #     similar_image = os.path.join(dir_compare,img)
        similar_image.append({
            'path':os.path.join(dir_compare,img),
            'ssim':float(ssim_index.item())
        })
    return sorted(similar_image,key= lambda d : d['ssim'],reverse=True)[start:end]
@csrf_exempt
def view_more_image(request):
    if is_logged_in(request.COOKIES.get('token')):
        data =request.POST
        image = data.get('image')
        name = data.get("name")
        start = int(data.get("start"))
        end = int(data.get("end"))
        print(start,end)
        model_name = Model.objects.get(isActive=True)

        dir_compare = os.path.join(DATASET,"{}\\val\\{}".format(model_name.dataset.path,name))
        image_path=f"tmp\\{image}"
        print(image_path)
        image_compare_list = get_similar_image(image_path=image_path,dir_compare=dir_compare,start=start,end=end)
     
        image_binary_list = []
        for image_compare in image_compare_list:
            image_read = open(image_compare['path'],'rb').read()
            image_binary = base64.b64encode(image_read)
            image_binary_list.append({'image':image_binary.decode('utf-8')})
        print(image_binary_list)
        return JsonResponse({'data':image_binary_list})
    
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
def search_disease(request):
    if request.method == 'GET':
        token = request.COOKIES.get("token")
        if token is None:
            # users = User.objects.all().values()
            # return JsonResponse(list(users), safe=False)
            return JsonResponse({"message": "Not login"}, status = 401)
        
        search_query = request.GET.get('query')
        if search_query is None:
            return JsonResponse({"message": "search_query parameter is required"}, status=400)
        
        result = Disease.objects.filter(name__icontains=search_query)
        if not result.exists():
            return JsonResponse({"message": "No diseases found with that name"}, status=404)
        
        return JsonResponse(list(result.values()), safe=False)
    else:
        return JsonResponse({"message": "Only GET method is allowed"}, status=405)