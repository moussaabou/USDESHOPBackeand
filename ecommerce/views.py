from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Admin, Seller, Product
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
import json

# ✅ عرض كل المنتجات مع الفلاتر
@api_view(['GET'])
def product_list(request):
    try:
        category = request.GET.get('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        order = request.GET.get('order', 'asc')

        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        products = products.order_by('price' if order == 'asc' else '-price')

        data = [
            {
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'category': p.category,
                'price': str(p.price),
                'images': [p.image1.url if p.image1 else None,
                           p.image2.url if p.image2 else None,
                           p.image3.url if p.image3 else None],
                'seller': p.seller.name,
            }
            for p in products
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ✅ تسجيل الدخول باستخدام JWT
@csrf_exempt
@api_view(['POST'])
def login_view(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    user = None
    role = None

    try:
        admin = Admin.objects.get(email=email)
        if admin.password == password:
            user = admin
            role = 'admin'
    except Admin.DoesNotExist:
        pass

    if not user:
        try:
            seller = Seller.objects.get(email=email)
            if seller.password == password:
                user = seller
                role = 'seller'
        except Seller.DoesNotExist:
            pass

    if not user:
        return JsonResponse({'error': 'بيانات الدخول غير صحيحة'}, status=400)

    refresh = RefreshToken.for_user(user)
    response_data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'role': role,
        'id': user.id
    }

    if role == 'seller':
        response_data.update({
            'name': user.name,
            'surname': user.surname,
            'phone_number': user.phone_number,
            'email': user.email,
            'address': user.address,
            'birth_date': str(user.birth_date),
            'profile_picture': user.profile_picture.url if user.profile_picture else None
        })

    return JsonResponse(response_data)

# ✅ تسجيل بائع جديد
@csrf_exempt
def register_seller(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            surname = request.POST['surname']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            address = request.POST['address']
            birth_date = request.POST['birth_date']
            password = request.POST['password']
            profile_picture = request.FILES.get('profile_picture', 'PIO.jpg')

            seller = Seller.objects.create(
                name=name,
                surname=surname,
                phone_number=phone_number,
                email=email,
                address=address,
                birth_date=birth_date,
                password=password,
                profile_picture=profile_picture,
            )
            return JsonResponse({'type': 'seller', 'id': seller.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# ✅ عرض منتجات بائع معيّن
@csrf_exempt
def seller_products(request, seller_id):
    products = Product.objects.filter(seller_id=seller_id)
    data = [
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'category': p.category,
            'price': str(p.price),
            'images': [p.image1.url if p.image1 else None,
                       p.image2.url if p.image2 else None,
                       p.image3.url if p.image3 else None]
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)

# ✅ إضافة منتج جديد
@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        try:
            product = Product(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                category=request.POST.get('category'),
                price=request.POST.get('price'),
                seller_id=request.POST.get('seller_id'),
            )
            for i in range(1, 4):
                img = request.FILES.get(f'image{i}')
                if img:
                    setattr(product, f'image{i}', img)
            product.save()
            return JsonResponse({'message': 'تمت إضافة المنتج بنجاح'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# ✅ حذف بائع (JWT + Admin)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_seller(request, seller_id):
    try:
        Admin.objects.get(email=request.user.email)
    except Admin.DoesNotExist:
        return JsonResponse({'error': 'غير مصرح'}, status=403)

    try:
        seller = Seller.objects.get(id=seller_id)
        Product.objects.filter(seller=seller).delete()
        seller.delete()
        return JsonResponse({'message': 'تم حذف البائع ومنتجاته'})
    except Seller.DoesNotExist:
        return JsonResponse({'error': 'البائع غير موجود'}, status=404)

# ✅ عرض كل البائعين
@api_view(['GET'])
def get_all_sellers(request):
    sellers = Seller.objects.all()
    data = [
        {'id': s.id, 'name': s.name, 'email': s.email, 'phone_number': s.phone_number}
        for s in sellers
    ]
    return JsonResponse(data, safe=False)

# ✅ عرض معلومات بائع + منتجاته
def get_seller_products(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    products = Product.objects.filter(seller=seller)

    product_data = []
    for p in products:
        images = [p.image1.url if p.image1 else None,
                  p.image2.url if p.image2 else None,
                  p.image3.url if p.image3 else None]
        product_data.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'description': p.description,
            'images': [img for img in images if img]
        })

    seller_data = {
        'name': seller.name,
        'surname': seller.surname,
        'email': seller.email,
        'phone_number': seller.phone_number,
        'address': seller.address,
        'birth_date': seller.birth_date.strftime('%Y-%m-%d'),
        'profile_picture': seller.profile_picture.url if seller.profile_picture else None
    }

    return JsonResponse({'seller_info': seller_data, 'products': product_data})

# ✅ تحديث منتج
@api_view(['PUT'])
@parser_classes([MultiPartParser])
def update_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.name = request.data.get('name', product.name)
        product.description = request.data.get('description', product.description)
        product.price = request.data.get('price', product.price)
        product.category = request.data.get('category', product.category)

        for i in range(1, 4):
            img = request.FILES.get(f'image{i}')
            if img:
                setattr(product, f'image{i}', img)

        product.save()
        return JsonResponse({'message': 'تم تحديث المنتج بنجاح'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'المنتج غير موجود'}, status=404)

# ✅ حذف منتج
@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'message': 'تم حذف المنتج'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'المنتج غير موجود'}, status=404)

# ✅ حذف صورة منتج محددة
@api_view(['POST'])
def delete_product_image(request, product_id, image_number):
    try:
        product = Product.objects.get(id=product_id)
        if image_number == 1:
            product.image1.delete(save=False)
            product.image1 = None
        elif image_number == 2:
            product.image2.delete(save=False)
            product.image2 = None
        elif image_number == 3:
            product.image3.delete(save=False)
            product.image3 = None
        else:
            return JsonResponse({'error': 'رقم الصورة غير صالح'}, status=400)

        product.save()
        return JsonResponse({'message': f'تم حذف الصورة {image_number}'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'المنتج غير موجود'}, status=404)

# ✅ عرض تفاصيل منتج
@api_view(['GET'])
def get_product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'price': str(product.price),
            'images': [
                product.image1.url if product.image1 else None,
                product.image2.url if product.image2 else None,
                product.image3.url if product.image3 else None,
            ],
            'seller': product.seller.name,
            'seller_id': product.seller.id,
            'seller_phone': product.seller.phone_number,
            'seller_address': product.seller.address,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'المنتج غير موجود'}, status=404)

# ✅ تحديث بيانات بروفايل بائع
@csrf_exempt
def update_seller_profile(request, seller_id):
    try:
        seller = Seller.objects.get(id=seller_id)
    except Seller.DoesNotExist:
        return JsonResponse({'error': 'البائع غير موجود'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'name': seller.name,
            'surname': seller.surname,
            'phone_number': seller.phone_number,
            'email': seller.email,
            'address': seller.address,
            'birth_date': str(seller.birth_date),
            'profile_picture': seller.profile_picture.url if seller.profile_picture else None,
        })

    elif request.method == 'POST':
        current_password = request.POST.get('current_password')
        if not current_password or current_password != seller.password:
            return JsonResponse({'error': 'كلمة المرور الحالية غير صحيحة'}, status=400)

        seller.name = request.POST.get('name', seller.name)
        seller.surname = request.POST.get('surname', seller.surname)
        seller.phone_number = request.POST.get('phone_number', seller.phone_number)
        seller.email = request.POST.get('email', seller.email)
        seller.address = request.POST.get('address', seller.address)
        seller.birth_date = request.POST.get('birth_date', seller.birth_date)

        new_password = request.POST.get('new_password')
        if new_password:
            seller.password = new_password

        if 'profile_picture' in request.FILES:
            seller.profile_picture = request.FILES['profile_picture']

        seller.save()
        return JsonResponse({'message': 'تم تحديث المعلومات بنجاح'})
