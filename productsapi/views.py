from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.contrib.auth.forms import UserCreationForm
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from .serializers import ProductSerializer
from webapp.models import Record
from webapp.forms import CreateRecordForm
from django.shortcuts import get_object_or_404


# Create your views here.
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def simpleapi(request):
    return Response({'text': 'Hello world, This is your first api call'},status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()  
    return Response({'message': 'Logout successful'}, status=HTTP_200_OK)

#api Create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    form = CreateRecordForm(request.POST)
    if form.is_valid():
        product = form.save()
        return Response({'id': product.id}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

#api read
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_products(request):
    products = Record.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

#api update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Record, pk=pk)
    form = CreateRecordForm(request.data, instance=product)
    if form.is_valid():
        form.save()
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
#api delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    try:
        product = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response("deleted successfully")

#api search
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def apisearch(request, mitem):
    medicines = Record.objects.filter(medicine_name__icontains=mitem)

    if medicines.exists():
        serializer = ProductSerializer(medicines, many = True)
        return Response(serializer.data)
    else:
        return Response({'error':'Medicine not found'}, status = HTTP_404_NOT_FOUND)

