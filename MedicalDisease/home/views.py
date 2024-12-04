from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import default_storage
from ultralytics.models import YOLO
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import cv2
import json
# Create your views here.
@csrf_protect
def home(request):
    template = loader.get_template('index.html')
    request.session.set_test_cookie()
    if request.method == 'POST' and request.FILES['image']:
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        image = request.FILES['image']
        image_path = default_storage.save('tmp/' + image.name, image)
        image_full_path = default_storage.path(image_path)
        model = YOLO("../models/yolov8-cls.pt")
        img = cv2.imread(image_full_path)
        results = model(img)
        r = []
        for result in results:
            print(result.summary())
            data = result.summary()
            data[0]["image"] = "urls"
            return JsonResponse({'data':data})
            # return HttpResponse(result.tojson())

    return HttpResponse(template.render())
