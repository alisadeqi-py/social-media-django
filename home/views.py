from django.shortcuts import get_object_or_404, render , redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post , Vote
from .forms import PostUpdateForm , PostCreateForm
from comments.forms import CommentForm , CommentReplyForm
from comments.models import Comment
# Create your views here.


class HomeView(View):

    def get(self , request):
        posts = Post.objects.all()
        return render(request , 'home/index.html' , {'posts':posts})

class PostDetailView(View):

    def setup(self , request , *args , **kwargs):
        self.post_instance = Post.objects.get(id = kwargs['id'] , slug = kwargs['slug'])
        return super().setup(request , *args , **kwargs)
    comment_form = CommentForm
    reply_form = CommentReplyForm
    def get(self , request, *args , **kwargs):
        post = self.post_instance
        comments = post.pcomments.filter(is_reply = False)
        return render(request , 'home/post-detail.html' , {'post':post , 'comments':comments ,
                                                            'form':self.comment_form , 'reply_form' : self.reply_form })
    method_decorator(login_required)
    def post(self , request , *args , **kwargs):
        form = self.comment_form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request , 'comment successfully')
            return redirect('home:post-detail' , self.post_instance.id , self.post_instance.slug)
        else:
            messages.error(request , 's.th is wrong')

class PostDeleteView(LoginRequiredMixin , View):

    def get(self , request , post_id):
        post = Post.objects.get(id = post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success( request , 'Post deleted successfully' , 'success')
        else:
            messages.error( request , 'you are not the owner' , 'error')

        return redirect('home:home')

class PostUpdateView(LoginRequiredMixin , View):

    form_class = PostUpdateForm

    def setup(self , request , *args, **kwargs):
         self.post_instance = Post.objects.get(id = kwargs['post_id'])
         super().setup(request , *args , kwargs)
    
    def dispatch(self , request ,*args, **kwargs):
        
        post = self.post_instance

        if not request.user.id == post.user.id:
            messages.error( request , 'ypu are not the owner' 'danger')
            return redirect('home:home')
        return super().dispatch(request , *args , **kwargs)
    def get(self, request , *args , **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request , 'home/update.html' , {'form':form})
    
    def post(self, request , *args , **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST , instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30]) 
            new_post.save()
            messages.success(request , 'you updated post successfuly' , 'success')
            return redirect('home:post-detail' ,  post.id , post.slug )
        
class PostCreateView(LoginRequiredMixin , View):
    
    form_class = PostCreateForm
    
    def get(self, request , *args , **kwargs):
        
        form = self.form_class
        print(form)
        return render( request , 'home/create.html' , {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            print(new_post)
            new_post.save()
            messages.success(request , 'post created' , 'success')
            return redirect('home:home')
        
class ReplyView(LoginRequiredMixin , View):

    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post , id = post_id)
        comment = get_object_or_404(Comment , id = comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.is_reply = True
            new_reply.post = post
            new_reply.comment = comment
            messages.success(request , 'comment added' , 'success')
        return redirect(request , 'home:post-detail' , post.id , post.slug)

class LikeView(LoginRequiredMixin , View):
    

    def get(self, request, post_id):

        post = get_object_or_404(Post , id = post_id)
        like = Vote.objects.filter(post = post_id)
        if like.exists():
            messages.error(request, 'you have liked this post', 'danger')
        else:
            Vote.objects.create(post=post , user=request.user)
            messages.success(request , 'you liked this post' , 'success')
        return redirect('home:post-detail' , post.id , post.slug )


