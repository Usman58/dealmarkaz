from django.shortcuts import render,HttpResponseRedirect
from .models import *
from django.db.models import Count
from django.shortcuts import render,get_object_or_404,reverse
from django.views import View
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.db.models import Q
# Create your views here.
class UserRegistrationView(View):
    def get(self,request):
        form=UserForm()
        return render(request,'Products/signup.html',{'form':form})
    def post(self,request):
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            print(user.id)
            group=Group.objects.get(name="Users")
            user.groups.add(group)
            messages.success(request,'Congratulations Registered successfully!')
            return HttpResponseRedirect('/products/accounts/login/')
        return render(request, 'Products/signup.html',{'form':form})


def create_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user=request.user
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                product=form.save(commit=False)
                product.owner=user
                product.save()
                p=Product.objects.get(id=product.id)
            images =request.FILES.getlist('images')
            for image in images:
                ProductImages.objects.create(product=p,image=image)
            return HttpResponseRedirect('/products/user/profile/')
        else:
            form=ProductForm()

        context = {'form':form}
        return render(request,'Products/createproduct.html',context)
    else:
        return HttpResponseRedirect('/products/accounts/login/')

def Productlist(request,c_slug=None):
    productlist=Product.objects.all().order_by('id')
    categorylist = Category.objects.annotate(total_products=Count('product'))
    if c_slug:
        category=Category.objects.get(slug=c_slug)
        productlist=Product.objects.filter(category=category)

    search_query=request.GET.get('q')

    if search_query:
        productlist=productlist.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)|
            Q(condition__icontains=search_query)|
            Q(brand__brand_name__icontains=search_query)|
            Q(category__category_name__icontains=search_query)|
           Q(owner__profile__city__icontains = search_query)
        )
    paginator = Paginator(productlist, 3, orphans=1)
    print(paginator)
    page_number = request.GET.get('page')

    productlist = paginator.get_page(page_number)
    context={
       'productlist': productlist,
        'categorylist':categorylist,
    }
    return render(request,'Products/product_list.html',context)

def ProductDetail(request,pk):
    product=Product.objects.get(id=pk)
    product_images=ProductImages.objects.filter(product=product)
    product = get_object_or_404(Product,id=pk)
    liked=False
    if product.likes.filter(id=request.user.id).exists():
        liked=True
    context={
       'product': product,
        'product_images':product_images,
        'liked':liked,
    }
    return render(request,'Products/product_detail.html',context)

def update_product(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      product= Product.objects.get(pk=id)
      form = UpdateProductForm(request.POST, instance=product)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/products/')
    else:
      product = Product.objects.get(pk=id)
      form = UpdateProductForm(instance=product)
    return render(request, 'Products/updateproduct.html', {'form':form,'product':product})
  else:
    return HttpResponseRedirect('/products/accounts/login/')

# Delete Post
def delete_product(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      product = Product.objects.get(pk=id)
      product.delete()
      return HttpResponseRedirect('/products/')
  else:
    return HttpResponseRedirect('/login/')

def create_brand(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BrandForm(request.POST)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect('/products/createproduct/')
        else:
            form=BrandForm()

        context = {'form':form}
        return render(request,'Products/createbrand.html',context)
    else:
        return HttpResponseRedirect('/products/accounts/login/')

def LikeView(request,pk):
    product=get_object_or_404(Product,id=request.POST.get('ad_id'))
    liked=False
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        liked=False
    else:
        product.likes.add(request.user)
        liked=True
    return HttpResponseRedirect(reverse('product_detail',args=[str(pk)]))


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            u_form = EditUserProfileForm(request.POST,instance=request.user)
            p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
            myproducts =Product.objects.filter(owner=user)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your Profile has been Updated Successfully')
        else:
            u_form = EditUserProfileForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
            user = request.user
            myproducts = Product.objects.filter(owner=user)
        context= {'name': request.user.username, 'p_form': p_form, 'u_form': u_form, 'myproducts': myproducts}
        return render(request, 'Products/profile.html',context)
    else:
        return HttpResponseRedirect('/products/')


def user_detail(request,pk):
  if request.user.is_authenticated:
      user = User.objects.get(id=pk)
      products=Product.objects.filter(owner=user)
      return render(request, 'Products/userdetails.html', {'user': user,'products':products})
  else:
      return HttpResponseRedirect('/products/accounts/login/')

def deleteUserProfile(request,pk):
  if request.user.is_authenticated:
    if request.method == 'POST':
      user= User.objects.get(id=pk)
      user.delete()
      if request.user.is_staff==True:
          messages.success(request, 'User has been Deleted Successfully')
          return HttpResponseRedirect('/products/user/profile')
      else:
          messages.success(request, 'Your Account has been Deleted Successfully')
          return HttpResponseRedirect('/products/signup/')

  else:
    return HttpResponseRedirect('/login/')
