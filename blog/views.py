from django.shortcuts import  render, redirect
from .forms import NewUserForm,PostForm,SearchForm
from .models import Post
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("http://127.0.0.1:8000/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}.")
                return redirect("/welcome")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


class WelcomePageView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'welcome.html'
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        con = super(WelcomePageView, self).get_context_data(**kwargs)
        con['search']=SearchForm()
        return con



def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("http://127.0.0.1:8000/")



class CreatePostView(LoginRequiredMixin,CreateView): 
    model = Post
    form_class = PostForm
    template_name = 'addpost.html'
    success_url = ('/welcome')
   

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SearchUserView(LoginRequiredMixin,ListView): 
    model = Post
    template_name = 'searchresult.html'

    def get_queryset(self):
        name = self.request.GET.get('search','')
        if not User.objects.filter(username=name).exists():
            return None
        uid=User.objects.get(username=name)
        object_list = self.model.objects.all()
        if name:
            object_list = object_list.filter(Q(author=uid.id) & Q(public=True))
        return object_list

    