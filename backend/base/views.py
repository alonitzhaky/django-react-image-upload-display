# Imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import TaskSerializer
from .models import Task
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import JsonResponse

# Present all images to client
@api_view(['GET'])
def getTasks(request):
    res = [] #create an empty list
    for img in Task.objects.all(): #run on every row in the table...
        res.append({"title":img.title,
                    "description":img.description,
                    "completed":False,
                    "image":str(img.image)
                }) #append row by to row to res list
    return Response(res) #return array as json response
    
# upload image method (post)
class ImageUpload(APIView):
    parser_class=(MultiPartParser,FormParser)
    def post(self,request,*args,**kwargs):
        api_serializer=TaskSerializer(data=request.data)
        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('error',api_serializer.errors)
            return Response(api_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,*args,**kwargs):
        pass

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
def  register(req):
    username=req.data["username"]
    password=req.data["password"]
    # create a new user (encrypt password)
    try:
        User.objects.create_user(username=username,password=password)
    except:
        return Response("error")    
    return Response(f"{username} registered")
 
@api_view(['GET'])
def test(req):
    return Response("hello")

# /////////// Tasks table (CRUD)
@api_view(['GET','POST','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def tasks(req,id=-1):
    if req.method =='GET':
        user= req.user
        if id > -1:
            try:
                temp_task=user.task_set.get(id=id)
                return Response (TaskSerializer(temp_task,many=False).data)
            except Task.DoesNotExist:
                return Response ("not found") 
        
        all_tasks=TaskSerializer(user.task_set.all(),many=True).data
        return Response ( all_tasks)
        
    if req.method =='POST':
        print(type( req.user))
        Task.objects.create(title =req.data["title"],description=req.data["description"],completed= req.data["completed"],user=req.user)
        return Response ("post...")

    if req.method =='DELETE':
        user= req.user
        try:
            temp_task=user.task_set.get(id=id)
        except Task.DoesNotExist:
            return Response ("not found")    
        
        temp_task.delete()
        return Response ("del...")
    if req.method =='PUT':
        user= req.user
        try:
            temp_task=user.task_set.get(id=id)
        except Task.DoesNotExist:
            return Response ("not found")
        
        old_task = user.task_set.get(id=id)
        old_task.title =req.data["title"]
        old_task.completed =req.data["completed"]
        old_task.description=req.data["description"]
        old_task.save()
        return Response("res")