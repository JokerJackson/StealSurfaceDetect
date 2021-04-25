from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
from datetime import datetime

from django.shortcuts import render
import os
from users.views import index

from StealSurface_v1_2.settings import MEDIA_ROOT, MEDIA_URL
from users.models import LeastLogin, User, Image, DetectImage
from detect import detect


# Create your views here.


# 登录
def login(request):
    if request.method == 'POST':
        email = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(email=email)
        if user:
            if password == user[0].password:
                LeastloginTime = LeastLogin()
                LeastloginTime.user_id = user[0].id
                LeastloginTime.loginTime = datetime.now()
                LeastloginTime.save()

                request.session["upload_flog"] = 0
                return redirect(index, id=user[0].id)

                # return render(request, "index.html", context=result)
            else:
                errorMsg = {
                    'name': '登录失败',
                    'bec': '密码错误',
                    'means': '联系管理员'
                }
                return render(request, 'error.html', context=errorMsg)
        else:
            errorMsg = {
                'name': '登录失败',
                'bec': '用户不存在',
                'means': '联系管理员'
            }
            return render(request, 'error.html', context=errorMsg)
#
#
# 上传图片
def uploadImg(request, user_id):
    if request.method == 'POST':

        img = request.FILES.get('img_file')
        if img is None:
            request.session["error_filenull_flog"] = 1
            request.session["upload_flog"] = "0"  # 1代表上传了图片upload标志
            request.session["detect"] = 0
            return redirect(index, id=user_id)
        else:
            request.session["upload_flog"] = "1"  # 1代表上传了图片upload标志
            save_path = "%s/upload/%s/%s" % (MEDIA_ROOT, user_id, img.name)
            user = User.objects.filter(id=user_id)
            if not os.path.exists("%s/upload/%s/" % (MEDIA_ROOT, user_id)):
                os.makedirs("%s/upload/%s/" % (MEDIA_ROOT, user_id))
            all_upload_image_path = "%s/upload/%s" % (MEDIA_ROOT, user_id)
            images_list = os.listdir(all_upload_image_path)
            if img.name in images_list:
                request.session["error_sameName_flog"] = 1
                request.session["upload_flog"] = "0"
                return redirect(index, id=user_id)
            else:
                with open(save_path, 'wb') as f:
                    for content in img.chunks():
                        f.write(content)
                uploadImage = Image()
                uploadImage.user_id = user_id
                uploadImage.img_url = '%s/%s' % (user_id, img.name)
                uploadImage.uploadTime = datetime.now()
                uploadImage.save()
                request.session["detect"] = 1
            return redirect(index, id=user_id)


# 检测
def detectImg(request, user_id):
    if request.method == "POST":
        if request.session["detect"] == 1:
            user = User.objects.filter(id=user_id)  # 根据传过来的user_id查找用户
            images = Image.objects.filter(user_id=user_id) # 查找当前用户上传的图片
            image_url = images[len(images)-1].img_url   # 最近一次上传的图片的地址
            image_id = images[len(images)-1].id  # 图片的id
            detect_image = DetectImage()
            image_path = '%s/upload/%s'%(MEDIA_ROOT, image_url)  # 图片的完整地址
            image_name = str(image_url).split("/")[1] # 图片的文件名
            save_path = '%s/detect/%s/'%(MEDIA_ROOT, user_id) # 检测后的图片保存地址
            detect(o_source=image_path, o_project=save_path)
            # detect_img = detect_img = '%s%s'%(save_path, image_name)
            detectImg_url = "%s/%s"%(user_id, image_name)
            detect_image.image_id = image_id
            detect_image.detectText_url = "%s/labels/%s.txt"%(user_id, image_name[:-4])
            detect_image.detectImg_url = detectImg_url
            detect_image.save()
            request.session["detect_flog"] = "2"
            request.session["detect"] = 0
            return redirect(index, id=user_id)
        if request.session["detect"] == 0:
            request.session["detect_error_msg"] = 1
            return redirect(index, id=user_id)