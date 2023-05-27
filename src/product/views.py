from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from django.utils import timezone


# Create your views here.

from .models import (Category, Product, Images, Comment, Variant, FAQ)
from .forms import CommentForm
from order.models import Cart, Order

from order.forms import CartForm
from product.forms import SearchForm

def home_page(request):
    category = Category.objects.all()
    product_slide = Product.objects.all().order_by('id')[:4]
    latest_product = Product.objects.all().order_by('-id')[:4]
    picked_product = Product.objects.all().order_by('?')[:4]
    context = {
                'category': category,
                'product_slide': product_slide,
                'latest_product': latest_product,
                'picked_product': picked_product,
            }
    return render(request, 'product/home_page.html', context)


def category_product(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {
        'products' : products,
        'category': category,
    }
    return render(request, 'product/category_product.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.all()
    context = {
        'product' : product,
        'category': category,
        'images': images,
        'comments': comments,
    }

    if product.variant_choice != None:
        if request.method == "POST":
            variant_id = request.POST.get('variantid')
            variant = Variant.objects.get(id=variant_id)
            colors = Variant.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variant.objects.raw('SELECT * FROM quadshop_variant WHERE product_id=%s GROUP BY size_id', [id])
        else:
            variants = Variant.objects.filter(product_id=id)
            colors = Variant.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variant.objects.raw('SELECT * FROM quadshop_variant WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variant.objects.get(id=variants[0].id)

        context.update({
            'sizes': sizes, "colors": colors, "variant": variant
        })

    return render(request, 'product/product_detail.html', context)

def ajax_variant(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variant.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    # check if the method is post
    if request.method == 'POST': 
        form = CommentForm(request.POST)
        if form.is_valid():
            # creating relation between models and forms
            # data.save(commit=False)
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.content = form.cleaned_data['content']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            data.user_id = request.user.id
            data.save()
            messages.success(request, "Your comment has been succesfully added, Thank you")

            return HttpResponseRedirect(url)
        messages.error(request, "Kindly revise your post info")
    return HttpResponseRedirect(url)


def add_to_cart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    product = Product.objects.get(pk=id)

    product_in_cart = Cart.objects.filter(product=product, user=current_user)
    if product_in_cart:
        control=1
    else:
        control=0
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            # update order
            if control == 1:
                data = Cart.objects.get(product_id=id)
                # data.save(commit=False)
                data.quantity += form.cleaned_data['quantity']
                data.save()

                messages.success(request, "Product Sucessfully Updated")
            # create new order
            else:
                data = Cart()
                # data.save(commit=False)
                data.user = current_user
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.success(request, "Product was Sucessfully Added to cart")
        return HttpResponseRedirect(url)

    else:
        product = get_object_or_404(Product, pk=id)
        order_product, created = Cart.objects.get_or_create(
            product=product,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.cart.filter(product__slug=product.slug).exists():
                order_product.quantity += 1
                order_product.save()
                messages.info(request, "Product quantity was updated.")
                return HttpResponseRedirect(url)
            else:
                order.cart.add(order_product)
                messages.info(request, "Product was added to your cart.")
                return HttpResponseRedirect(url)

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.cart.add(order_product)
            messages.info(request, "This item was added to your cart.")
            return HttpResponseRedirect(url)


def remove_single_quantity_product(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    product = Product.objects.get(pk=id)
    cart, create = Cart.objects.get_or_create(
                        product=product, 
                        user=request.user, 
                        ordered=False) 

    order_qs = Order.objects.filter(user=request.user,ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.cart.filter(product__slug=product.slug).exists():
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
                messages.success(request, "Product was successfully deducted")
                return HttpResponseRedirect(url)

            else:
                # order.cart.remove(product)
                cart.delete()
                messages.success(request, "Product was successfully removed")
                return HttpResponseRedirect(url)
        
        else:
            messages.error(request, "Invalid request")
            return HttpResponseRedirect(url)
      

def remove_product_from_cart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    product = Product.objects.get(pk=id)
    cart = Cart.objects.filter(user=request.user, ordered=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        qs = order_qs[0].cart.filter(product__slug=product.slug)
        if qs.exists():
            qs.delete()
            messages.success(request, "Product was successfully removed")
            return HttpResponseRedirect(url)
    
    else:
        messages.error(request, "Invalid request")
        return HttpResponseRedirect(url)
    
def navbar(request):
    category = Category.objects.all()
    return render(request, 'navbar.html', context={'category':category})


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] 
            category_id = form.cleaned_data['category_id'] 
            if category_id == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query,
                                             category_id=category_id)
            category = Category.objects.all()
            context = {
                'products': products,
                'query': query,
                'category': category,
            }
            return render(request, 'product/search_product.html', context)
    return HttpResponseRedirect('/')



def faq(request):
    faq = FAQ.objects.all()
    context = {
        'faq': faq
    }
    return render(request, 'product/faq.html', context)
