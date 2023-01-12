# Imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer
from .models import Product
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

# Present all images to client
@api_view(['GET'])
def get_product(request):
    res = [{"title": item.title, "description": item.description, "price": item.price, "image": str(item.image)} for item in Product.objects.all()]
    return Response(res) #return array as json response

# upload image method (post)
class ImageUpload(APIView):
    parser_class=(MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        api_serializer=ProductSerializer(data=request.data, context = {'user': request.user})
        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('error',api_serializer.errors)
            return Response(api_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request,*args,**kwargs):
    #     pass

# Login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Register
@api_view(['POST'])
def register(request):
    username=request.data["username"]
    password=request.data["password"]
    # create a new user (encrypt password)
    try:
        User.objects.create_user(username=username,password=password)
    except:
        return Response("error")    
    return Response(f"{username} registered")
 
# /////////// product table (CRUD)
@api_view(['GET','POST','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def product(request,id=-1):
    if request.method =='GET':
        user= request.user
        if id > -1:
            try:
                temp_product=user.product_set.all()
                return Response (ProductSerializer(temp_product,many=False).data)
            except Product.DoesNotExist:
                return Response ("not found") 
        
        all_tasks=ProductSerializer(user.product_set.all(),many=True).data
        return Response ( all_tasks)
        
    if request.method =='POST':
        print(type( request.user))
        product.objects.create(title =request.data["title"], description=request.data["description"], completed= request.data["price"], user=request.user)
        return Response ("post...")

    if request.method =='DELETE':
        user= request.user
        try:
            temp_product=user.product_set.get(id=id)
        except Product.DoesNotExist:
            return Response ("not found")    
        
        temp_product.delete()
        return Response ("del...")
    if request.method =='PUT':
        user= request.user
        try:
            temp_product=user.product_set.get(id=id)
        except Product.DoesNotExist:
            return Response ("not found")
        
        old_product = user.task_set.get(id=id)
        old_product.title =request.data["title"]
        old_product.completed =request.data["price"]
        old_product.description=request.data["description"]
        old_product.save()
        return Response("The update was successfuly")

# API View
@permission_classes([IsAuthenticated])
class MyModelView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        my_product = Product.objects.all()
        serializer = ProductSerializer(my_product, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        # usr =request.user
        # print(usr)
        serializer = ProductSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        my_product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(my_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        my_product = Product.objects.get(pk=pk)
        my_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
