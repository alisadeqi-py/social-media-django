from django.shortcuts import render
from django.views import View
from .forms import UserRegisterationForm , UserLoginForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from .models import Relation 
# Create your views here.

class UserRegisterView(View):

    form_class = UserRegisterationForm

    def dispatch(self, request , *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request , *args , **kwargs)

    def get(self , request):
        form = self.form_class()
        return render(request , 'account/register.html' , {'form':form})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'] , cd['email'] , cd['password'])
            messages.success(request , 'you registered succsessfully' , 'success')
            return redirect('home:home')
        return render(request , 'account/register.html' , {'form':form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'


    def setup(self, request , *args, **kwargs):
        self.next = request.GET.get('next' , None)  
        
        return super().setup(request, *args, **kwargs)

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})
    
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username=cd['username'] 
                              , password=cd['password'])
            if user is not None:
                login(request , user)
                messages.success(request , 'you logged in successfully' , 'succsses')
                if self.next == next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request , 'username or password is wrong' , 'warning')
        return render(request , self.template_name , {'form':form})


class UserLogoutView(View):
    
    def get(self , request):
        logout(request)
        messages.success( request , 'you loged out successfuly' , 'success')
        return redirect('home:home')
    
class UserProfileView(LoginRequiredMixin , View ):
    
    def get(self  , request , user_id):
        is_following = False
        user = User.objects.get(id = user_id)
        posts = Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)  
        if relation.exists():
            is_following = True
        return render(request , 'account/profile.html' , {'user':user , 'posts':posts , 'is_following': is_following})
    

class UserFollowView(LoginRequiredMixin , View):

    def get(self , request , user_id):
        user = User.objects.get(id = user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            messages.error(request , 'you are following this user')
        else:
            Relation.objects.create(from_user = request.user , to_user = user)
            messages.success(request , 'you followed this user')
        return redirect( 'account:userprofile' , user_id)

class UserUnfollowView(LoginRequiredMixin , View):

    def get(self  , request , user_id):
        user = User.objects.get(id = user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            relation.delete()
            messages.success(request , 'successfully unfollowed')
        else:
            messages.error(request , 'you didnot follow this user')
        return redirect('account:userprofile' , user_id)
    
