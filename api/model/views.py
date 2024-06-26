import cv2
import json
import base64
import os
import torch 
import asyncio
from datetime import datetime
from asgiref.sync import async_to_sync
from os import listdir
from django.shortcuts import render
from urllib.parse import parse_qs
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from api.model.models import Model,Dataset,Disease,Request,Question,Anwser,QuestionInstance
from api.user.models import Department
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
from urllib.parse import parse_qs

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
        # print("model",model_name.path)
        response = []
        # print(decode_token(token))
        id = request.POST.get("id")
        print("id",id)
        for image in request.FILES.getlist('image'):
            # print("image",image)
            image_path = default_storage.save('tmp/' + image.name, image)
            image_full_path = default_storage.path(image_path)
            
            img = cv2.imread(image_full_path)
            results = predict_image(model=model,image=img)
            user = User.objects.get(id=cookie["id"])
            # request = Request.objects.create(user=user,content="this is my request",image=image_path)
            # print(request)
            result = results[0]
                # print(result.summary())
            datas = result.summary()
            
            for data in datas:
                # if data['confidence'] < 0.5:
                #     continue
                dir_compare = os.path.join(DATASET,"{}\\val\\{}".format(model_name.dataset.path,data["name"]))

                image_compare_list = get_similar_image(image_path=image_full_path,dir_compare=dir_compare,end=5)
              
                image_binary_list = []
                for image_compare in image_compare_list:
                    image_read = open(image_compare['path'],'rb').read()
                    image_binary = base64.b64encode(image_read)
                    image_binary_list.append({'image':image_binary.decode('utf-8')})
                data["id"] = int(id)
                data["image_name"] = image.name
                data["image_base64"] = image_binary_list
                try:
                    label = Disease.objects.filter(name=data['name']).values().first()
                    data["label"] = label["label"]
                    data["disease_id"] = label["id"]
                    # print(label)
                except:
                    print(f"not fount" + data["name"])
                    pass
                # print(data['confidence'])
                response.append(data)
        print("done")
        if len(response) == 0 :
            return JsonResponse({"error":True},status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(response,status = status.HTTP_200_OK,safe=False)
    return JsonResponse({"msg":"get request"})

def predict_image(model,image):
    return model(image)

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
        return JsonResponse(
            {"msg":"must be logged in"},
            status=status.HTTP_401_UNAUTHORIZED)
    
    if not is_supperuser(request):
        return JsonResponse(
            {"msg":"permission not allowed"},
            status=status.HTTP_403_FORBIDDEN)
    
    try:
        model = list(Model.objects.all().values())
        print(model)
        return JsonResponse(model,safe=False,status=status.HTTP_200_OK)
    except:
        return JsonResponse(
            {"msg":"model not found"},
            status=status.HTTP_404_NOT_FOUND)
    
@require_http_methods(["GET"])
def get_active_model(request):
    token = request.COOKIES.get("token")
    if token is None:
        return JsonResponse(
            {"msg":"must be logged in"},
            status=status.HTTP_401_UNAUTHORIZED)
    
    if not is_supperuser(request):
        return JsonResponse({"msg":"permission not allowed"},
                            status=status.HTTP_403_FORBIDDEN)
    
    try:
        model = Model.objects.filter(isActive=True).values().first()
        try:
            dataset = Dataset.objects.filter(id=model["dataset_id"]).values().first()
        except Dataset.DoesNotExist:
            dataset = None
        data = {
            "path":model["path"],
            "accuracy":model["accuracy"],
            "class":dataset["class_num"]}
        print("active",data)
        # print(model)
        return JsonResponse(data,safe=False,status=status.HTTP_200_OK)
    except Model.DoesNotExist as err:
        print(err)
        return JsonResponse({"msg":"model not found"},status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@require_http_methods(["POST"])
def change_active_model(request):
    token = request.COOKIES.get("token")
    id = request.POST.get("id")
    print(id)
    if not is_logged_in(token):
        return JsonResponse(
            {"msg":"must be logged in"},
            status=status.HTTP_401_UNAUTHORIZED)
    
    if not is_supperuser(request):
        return JsonResponse(
            {"msg":"permission not allowed"},
            status=status.HTTP_403_FORBIDDEN)
    try:
        old_active = Model.objects.get(isActive=True)
        old_active.isActive = False
        old_active.save()

    except Model.DoesNotExist:
        old_active = None

    try:
        active = Model.objects.get(id=id)
        active.isActive = True
        active.save()
        print(active)
    except Model.DoesNotExist:
        active = None

    if not active:
        return JsonResponse(
            {"msg":"active model doesn't exists"},
            status=status.HTTP_404_NOT_FOUND)
    
    return JsonResponse(
        {"msg":"update active model successfull"},
        status=status.HTTP_200_OK)

@require_http_methods(["GET"])
def get_all_dataset(request):
    token = request.COOKIES.get("token")
    if token is None:
        return JsonResponse({"msg":"must be logged in"},
                            status=status.HTTP_401_UNAUTHORIZED)
    
    permission = get_permission(token=token)
    if permission != 'admin':
        return JsonResponse({"msg":"permission not allowed"},
                            status=status.HTTP_403_FORBIDDEN)
    
    try:
        dataset = list(Dataset.objects.all().values())
        print(dataset)
        return JsonResponse(dataset,status=status.HTTP_200_OK,safe=False)
    except:
        return JsonResponse({"msg":"dataset not found"},
                            status=status.HTTP_404_NOT_FOUND)


@require_http_methods(["POST"])
@csrf_exempt
def create_new_disease(request):
    if not is_supperuser(request=request):
        return JsonResponse({"msg":"permission not allowed"},
                            status=status.HTTP_403_FORBIDDEN)
    
    name = request.POST.get("name")
    description = request.POST.get("description")
    type = request.POST.get("type")

    try:
        disease = Disease.objects.create(name=name,description=description,type=type)
        print(disease)
        return JsonResponse({"msg":"create new disease successfull"},
                            status = status.HTTP_201_CREATED,safe=False)
    except:
        return JsonResponse({"msg":"Cannot create new disease"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@require_http_methods(['POST'])
@csrf_exempt
def update_disease(request,id):
    if not is_supperuser(request=request):
        return JsonResponse({"msg":"permission not allowed"},
                            status=status.HTTP_403_FORBIDDEN)
    name = request.POST.get("name")
    description = request.POST.get("description")
    type = request.POST.get("type")
    print(id)
    try:
        disease = Disease.objects.get(id=id)
    except:
        return JsonResponse({"msg":"disease with id not found"},
                            status=status.HTTP_404_NOT_FOUND)
    
    try:
        disease.name = name
        disease.description = description
        disease.type = type
        disease.save()
    except Exception as e:
        print(e)
        return JsonResponse({"msg":"update disease error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JsonResponse({"id":id},status = status.HTTP_200_OK,safe=False)


def add_data(request):
    with open(f"{DATASET}/data.json","r",encoding='utf-8') as f:
        data:dict
        data = json.load(f)
        for key,value in data.items():
            # print(key)
            try:
                d = Disease.objects.get(name=key)
                continue
            except:
                disease = Disease(
                    name=key,
                    label=value["label"],
                    concept= value["concept"],
                    reason = value["reason"],
                    symptom = value["symptom"],
                    consequence = value["consequence"],
                    type = value["type"]
                )
                disease.save()

                print(disease)
            # break
    f.close()
    return JsonResponse({})

def get_all_diseases(request):
    if not is_supperuser(request):
        return JsonResponse({"msg":"permission not allowed"},
                            status=status.HTTP_403_FORBIDDEN)

    try:
        disease = list(Disease.objects.all().values())
        print(type(disease))
    except Disease.DoesNotExist:
        return JsonResponse({"msg":"disease not found"},status=status.HTTP_404_NOT_FOUND)

    return JsonResponse(disease,safe=False,status=status.HTTP_200_OK)

def get_disease(request,id):
    token = request.COOKIES.get("token")
    if not is_logged_in(token):
        return JsonResponse({"msg":"not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        disease = Disease.objects.filter(id=id).values().first()
        # print(disease)
    except Disease.DoesNotExist:
        return JsonResponse({},status=404)
    return  JsonResponse(disease,safe=False,status=200)

def get_dataset(request,id):
    return JsonResponse({})

@require_http_methods(["POST"])
@csrf_exempt
def send_question(request):
    token = request.COOKIES.get("token")
    if not is_logged_in(token):
        return JsonResponse({"msg":"not logged in"},status=401)
    id = decode_token(token)["id"]
    content = request.POST.get("content")
    image = request.FILES.get("image")
    name :str= image.name.replace(".jpg",datetime.now().strftime("%f") + ".jpg")
    image_path = default_storage.save(f"tmp/{name}",image)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        user = None
    try:
        question = Question(
            content=content,
            user = user,
            image = image_path
        )
        question.save()
    except KeyError as err:
        print(err)
    if( question is not None):
        return JsonResponse({"msg":"send request oke"},status=200)
    return JsonResponse({"msg":"something error"},status=400)

def get_question_by_state(request):
    token = decode_token(request.COOKIES.get("token"))
    if token is None:
        return JsonResponse({"msg":"not logged in"},status=400)
    
    # print(parse_qs(request.GET.urlencode()))
    query = parse_qs(request.GET.urlencode())
    state = query["state"][0]
    if(token["permission"] == "student"):
        return JsonResponse({"msg":"permission not allow"},status=403)
    
    try:
        if state == "all":
            questions = list(Question.objects.all().values())
        else:
            if state == "done":
                isAnwser = True
            else: isAnwser = False
            questions = list(Question.objects.filter(isAnwserd = isAnwser).values())
        print(questions)
    
    except Question.DoesNotExist as err:
        print(err)
        return JsonResponse({"msg":"not found"},status=404)
    
    for question in questions:
        image = question["image"]
        with open(image,"rb") as img:
            image_encode = base64.b64encode(img.read())
            image_decode = image_encode.decode("utf-8")
            question["image"] = image_decode
        created = question["created"]
        question["created"] = f'{created.strftime("%x")} {created.strftime("%X")}'
        try:
            user = User.objects.filter(id=question["user_id"]).values().first()
            name = user["name"]
        except User.DoesNotExist as err:
            print(err)
        question["name"] = name
        # print(question["name"])
    return JsonResponse(questions,safe=False,status=200)

@csrf_exempt
def get_question_by_process(request):
    token = decode_token(request.COOKIES.get("token"))
    if token is None:
        return JsonResponse({"msg":"not logged in"},status=400)
    
    # print(parse_qs(request.GET.urlencode()))
    query = parse_qs(request.GET.urlencode())
    state = query["state"][0]
    if(token["permission"] == "student"):
        return JsonResponse({"msg":"permission not allow"},status=403)
    
    try:       
        questions = list(Question.objects.all().values())
       
    except Question.DoesNotExist as err:
        print(err)
        return JsonResponse({"msg":"not found"},status=404)
    new_questions = []
    for question in questions:
        q = Question.objects.get(id=question["id"])
        is_exists  = QuestionInstance.objects.filter(question = q).exists()
        print(is_exists,len(questions),state)
        if state == "done" and not is_exists :
            continue
        elif state == "wait" and  is_exists:
            continue
        image = question["image"]
        with open(image,"rb") as img:
            image_encode = base64.b64encode(img.read())
            image_decode = image_encode.decode("utf-8")
            question["image"] = image_decode
        created = question["created"]
        question["created"] = f'{created.strftime("%x")} {created.strftime("%X")}'
        try:
            user = User.objects.filter(id=question["user_id"]).values().first()
            name = user["name"]
        except User.DoesNotExist as err:
            print(err)
        question["name"] = name
        # print(question["name"])
        new_questions.append(question)
    return JsonResponse(new_questions,safe=False,status=200)

@require_http_methods(["POST"])
@csrf_exempt
def send_anwser(request):
    token = request.COOKIES.get("token")
    if not is_logged_in(token):
        return JsonResponse({"msg":"not logged in"},status=401)
    user = decode_token(token)
    if user["permission"] != "officer":
        return JsonResponse({"msg":"permission not allow"},status=403)
    id = user["id"]
    content = request.POST.get("content")
    image = request.FILES.get("image")
    name :str= image.name.replace(".jpg",datetime.now().strftime("%f") + ".jpg")
    question_id = request.POST.get("question_id")
    image_path = default_storage.save(f"tmp/{name}",image)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        user = None
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist as err:
        print(err)
        return JsonResponse({"msg":"question dose not exists"},status=404)
    try:
        anwser = Anwser(
            user = user,
            question = question,
            image = image_path,
            content = content
            )
        anwser.save()
        print(question)
        question.isAnwserd = True
        question.save()
    except KeyError as err:
        print(err)
    if( anwser is not None):
        return JsonResponse({"msg":"send request oke"},status=200)

    return JsonResponse({"msg":"something error"},status=500)

@require_http_methods(["GET"])
def get_all_anwser(request):
    token = decode_token(request.COOKIES.get("token"))
    if token is None:
        return JsonResponse({"msg":"not logged in"},status=400)
    if(token["permission"] == "student"):
        return JsonResponse({"msg":"permission not allow"},status=403)
    
    try:
        anwsers = list(Anwser.objects.all().values())
        # print(anwsers)
    except Anwser.DoesNotExist as err:
        print(err)
        return JsonResponse({"msg":"not found"},status=404)
    
    for anwser in anwsers:
        image = anwser["image"]
        with open(image,"rb") as img:
            image_encode = base64.b64encode(img.read())
            image_decode = image_encode.decode("utf-8")
            anwser["image"] = image_decode
        created = anwser["created"]
        anwser["created"] = f'{created.strftime("%x")} {created.strftime("%X")}'
        try:
            user = User.objects.filter(id=anwser["user_id"]).values().first()
            name = user["name"]
        except User.DoesNotExist as err:
            print(err)
        anwser["name"] = name
        # print(anwser["name"])
    return JsonResponse(anwser,safe=False,status=200)

def get_anwser_by_user(request,id):
    if not is_logged_in(request.COOKIES.get("token")):
        return JsonResponse({"msg":"not logged in"},status=401)
    try:
        questions = list(Question.objects.filter(user_id = id).values())
        # print(question[0])
       
    except Question.DoesNotExist as err:
        print(err)
    res = []
    try:
        anwsers = list(Anwser.objects.all().values())
        for anwser in anwsers: 
            is_exists = False
            for question in questions:
                if anwser["question_id"] == question["id"]:
                    is_exists = True
                    break
            if is_exists:
                try:
                    user = User.objects.filter(id=anwser["user_id"]).values().first()

                except User.DoesNotExist as err:
                    user = None
                    print(err)
                anwser["name"] = user["name"]
                anwser["tag"] = "Anwser"
                res.append(anwser)
    except Anwser.DoesNotExist as err:
        print(err)
    # print(res)
    res.reverse()
    return JsonResponse(res,safe=False,status=200)

@require_http_methods(["POST"])
@csrf_exempt
def add_question_instance(request,question_id,department_id):
    print(question_id,department_id)
    try:
        department = Department.objects.get(id=department_id)

    except Department.DoesNotExist as err:
        print(err)
        return JsonResponse({"msg":"not found"},status=404)
    try:
        question = Question.objects.get(id=question_id)
    
    except Question.DoesNotExist as err:
        print(err)
        return JsonResponse({"msg":"not found"},status=404)
    try:
        question_instance = QuestionInstance.objects.create(question=question,department=department)
    except:
        print("error")
        return JsonResponse({"msg":"server error"},status=500)
    
    return JsonResponse({"msg":"successfull"},status=200)