from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,ListView,DetailView,
                                  CreateView,UpdateView,DeleteView)
from  blog.models import Post,Comment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from blog.forms import PostForm,CommentForm

# Create your views here.
class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model=Post

    def get_queryset(self):
        # this allows me to use django's ORM to query the database
        # __lte is a field lookup that means less than or equal to
        # -published_date means order by published date in descending order
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(LoginRequiredMixin,DetailView):
    model=Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=PostForm
    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name='blog/post_detail.html'
    form_class=PostForm
    model=Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('blog:post_list')
    # reverse_lazy is used because we don't want to execute the reverse function until the post is deleted

class DraftListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    redirect_field_name='blog/post_list.html'
    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')
        # __isnull is a field lookup that means is null ie post is not published yet
        # order by created date in ascending order


##############################################################################################################
'''
Now we need to create the views for the comments.
These are functional views 
They will be called when the user wants to approve or remove a comment
'''
##############################################################################################################



@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk) # this is how we get the post that we want to publish
    post.publish() # this is how we publish the post
    return redirect('blog:post_detail',pk=pk) # redirect to the post detail page


@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk) # this is how we get the post that we want to comment on
    if request.method=='POST': # if the form is submitted
        form=CommentForm(request.POST) # create a form instance with the submitted data
        if form.is_valid(): # check if the form is valid
            comment=form.save(commit=False) # create a comment object but don't save it to the database yet
            comment.post=post # this is how we connect the comment to the post
            comment.save() # save the comment to the database
            return redirect('blog:post_detail',pk=pk) # redirect to the post detail page
    else:  # agr form submit ni hua hai to form bnao aur dobara render kro
        form=CommentForm() # if the form is not valid then create a new form
    return render(request,'blog/comment_form.html',{'form':form}) # render the form again


@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk) # this is how we get the comment that we want to approve
    comment.approve() # approve the comment
    return redirect('blog:post_detail',pk=comment.post.pk) # redirect to the post detail page


@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk) # this is how we get the comment that we want to remove
    post_pk=comment.post.pk # get the pk of the post that the comment belongs to
    comment.delete() # delete the comment
    return redirect('blog:post_detail',pk=post_pk) # redirect to the post detail page

