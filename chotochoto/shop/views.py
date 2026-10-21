from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, Product


def catalog(request):
    products = Product.objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "shop/catalog.html", {"products": products, "query": query})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "shop/product.html", {"product": product})


def cart_rows(request):
    saved = request.session.get("cart", {})
    rows = []
    for product in Product.objects.filter(id__in=saved):
        quantity = int(saved[str(product.id)])
        rows.append({
            "product": product,
            "quantity": quantity,
            "subtotal": product.price * quantity,
        })
    return rows


def cart(request):
    rows = cart_rows(request)
    return render(request, "shop/cart.html", {
        "rows": rows,
        "total": sum(row["subtotal"] for row in rows),
    })


def cart_add(request, product_id):
    get_object_or_404(Product, id=product_id)
    saved = request.session.get("cart", {})
    key = str(product_id)
    saved[key] = saved.get(key, 0) + 1
    request.session["cart"] = saved
    return redirect("shop:cart")


def cart_update(request, product_id):
    saved = request.session.get("cart", {})
    try:
        quantity = int(request.GET.get("quantity", 0))
    except ValueError:
        quantity = 0
    if quantity > 0:
        saved[str(product_id)] = quantity
    else:
        saved.pop(str(product_id), None)
    request.session["cart"] = saved
    return redirect("shop:cart")


def checkout(request):
    rows = cart_rows(request)
    if not rows:
        return redirect("shop:cart")
    total = sum(row["subtotal"] for row in rows)
    error = ""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        if name and phone:
            order = Order.objects.create(
                name=name,
                phone=phone,
                items="\n".join(f'{row["product"].name}, {row["quantity"]} шт' for row in rows),
                total=total,
            )
            request.session["cart"] = {}
            return redirect("shop:thanks", order_id=order.id)
        error = "Введите имя и телефон"
    return render(request, "shop/checkout.html", {"rows": rows, "total": total, "error": error})


def thanks(request, order_id):
    return render(request, "shop/thanks.html", {"order_id": order_id})
