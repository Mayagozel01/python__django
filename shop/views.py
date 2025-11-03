from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Size, Color
from django.core.paginator import Paginator


def product_list(request):
	qs = Product.objects.select_related('category').prefetch_related('sizes', 'colors').all()

	# filters from GET
	category = request.GET.get('category')
	size = request.GET.get('size')
	color = request.GET.get('color')

	if category:
		qs = qs.filter(category__slug=category)
	if size:
		qs = qs.filter(sizes__name__iexact=size)
	if color:
		qs = qs.filter(colors__name__iexact=color)

	paginator = Paginator(qs.distinct(), 12)
	page = request.GET.get('page')
	products = paginator.get_page(page)

	context = {
		'products': products,
		'categories': Category.objects.all(),
		'sizes': Size.objects.all(),
		'colors': Color.objects.all(),
		'current_filters': {'category': category, 'size': size, 'color': color},
	}
	return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	return render(request, 'shop/product_detail.html', {'product': product})


# Simple session-based cart
def cart_add(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	cart = request.session.get('cart', {})
	str_id = str(product_id)
	cart[str_id] = cart.get(str_id, 0) + 1
	request.session['cart'] = cart
	return redirect('shop:cart_detail')


def cart_remove(request, product_id):
	cart = request.session.get('cart', {})
	str_id = str(product_id)
	if str_id in cart:
		del cart[str_id]
		request.session['cart'] = cart
	return redirect('shop:cart_detail')


def cart_detail(request):
	cart = request.session.get('cart', {})
	product_ids = [int(pid) for pid in cart.keys()]
	products = Product.objects.filter(id__in=product_ids)
	items = []
	total = 0
	for p in products:
		qty = cart.get(str(p.id), 0)
		subtotal = p.price * qty
		total += subtotal
		items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})

	return render(request, 'shop/cart.html', {'items': items, 'total': total})

