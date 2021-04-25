from django.shortcuts import render, redirect

# Create your views here.
from StealSurface_v1_2.settings import MEDIA_ROOT
from users.models import LeastLogin, User, Image, DetectImage


def login_index(request):
    return render(request, 'login.html')

def index(request, id):
    detect_texts = []
    # 上传图片的路径
    image_url = ''    # 上传图片的路径
    detect_image_url = ''    # 检测结果的图片路径
    detect_text_url = ''
    e_sameName_flog = 0    # 上传的图片已存在的标志
    uploadImg_flog = 0    # 上传完图片的标志
    detectImg_flog = 0    # 检测完的图片的标志
    error_filenull_flog = 0    # 上传图片为空的标志
    detect_error_msg = 0
    result_list = []    # 结果保存的列表
    # request.session["detect_flog"] = "0"
    # request.session["upload_flog"] = "0"
    # request.session["error_filenull_flog"] = 0
    # request.session["error_sameName_flog"] = 0
    # request.session["detect_error_msg"] = 0
    user_login = LeastLogin.objects.filter(user_id=id)  # 用户登录时间表
    user = User.objects.filter(id=id)     # 用户表
    image = Image.objects.filter(user_id=id)   # 获取当前用户的图片

    # detect_image = DetectImage.objects.get(image_id=image_id)
    if request.session["error_filenull_flog"] == 1:    # 判断session中上传文件是否为空
        error_filenull_flog = 1     # 如果为空，前端文件为空的标志
        request.session["error_filenull_flog"] = 0    # 重置session中error_filenull_flog 为 0
    if request.session["error_sameName_flog"] == 1:    # 判断session中是否上传过当前文件
        e_sameName_flog = 1    # 如果为空，标志为1
        request.session["error_sameName_flog"] = 0   # 重置session中error_sameName_flog 为 0
    if request.session["upload_flog"] == "1":    # 判断是否上传了图片
        image_url = image[len(image) - 1].img_url  # 获得最新的
        uploadImg_flog = 1    # 如果上传了图片
        request.session["upload_flog"] = "0"
    if request.session["detect_error_msg"] == 1:
        detect_error_msg = 1
        request.session["detect_error_msg"] = 0
    if request.session["detect_flog"] == "2":
        image_id = image[len(image) - 1].id
        detect_image_url = DetectImage.objects.filter(image_id=image_id)[0].detectImg_url
        detect_text_url = DetectImage.objects.filter(image_id=image_id)[0].detectText_url
        text_url = "%s/detect/%s"%(MEDIA_ROOT, detect_text_url)
        detect_text = open(text_url)
        detect_texts = detect_text.readlines()
        for i in detect_texts:
            text_list = ["检测结果为: ", i.split(",")[4], "\t", "置信度为：", i.split(",")[-1].strip().split(":")[1]]
            result_list.append(text_list)
        image_url = image[len(image) - 1].img_url  # 获得最新的
        uploadImg_flog = 1
        detectImg_flog = 1
        request.session["detect_flog"] = "0"
    if len(user_login) < 2:
        least = '欢迎您登录系统'
    else:
        least = user_login[len(user_login) - 2].loginTime
    result = {
        'user': user[0],
        'leastTime': least,
        'img_url': "upload/%s"%image_url,
        'uploadImg_flog': uploadImg_flog,
        'detectImg_flog': detectImg_flog,
        'detectImg_url': "detect/%s"%detect_image_url,
        "detect_text": result_list,
        "total": len(result_list),
        "error_filenull_flog": error_filenull_flog,
        "error_sameName_flog": e_sameName_flog,
        "detect_error_msg": detect_error_msg
    }
    return render(request, 'index.html', result)