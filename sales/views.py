from decimal import Decimal
from urllib.parse import quote
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Shop, Order, OrderItem

def dashboard(request):
    orders = Order.objects.select_related("shop","salesman").order_by("-order_date")[:20]
    total_sales = Order.objects.aggregate(x=Sum("total_amount"))["x"] or 0
    pending = sum(o.pending_amount for o in orders)
    return render(request, "dashboard.html", {
        "orders": orders, "total_sales": total_sales, "pending": pending,
        "shop_count": Shop.objects.count(), "product_count": Product.objects.filter(active=True).count()
    })

def new_visit(request):
    products = Product.objects.filter(active=True).order_by("name")
    if request.method == "POST":
        shop = Shop.objects.create(
            name=request.POST.get("shop_name",""),
            owner_name=request.POST.get("owner_name",""),
            phone=request.POST.get("phone",""),
            address=request.POST.get("address",""),
            shop_photo=request.FILES.get("shop_photo"),
            card_photo=request.FILES.get("card_photo"),
        )
        order = Order.objects.create(
            shop=shop,
            salesman=request.user if request.user.is_authenticated else None,
            payment_method=request.POST.get("payment_method","cash"),
            paid_amount=Decimal(request.POST.get("paid_amount") or 0),
        )
        total = Decimal("0")
        for product in products:
            qty = int(request.POST.get(f"qty_{product.id}") or 0)
            if qty > 0:
                subtotal = product.price * qty
                OrderItem.objects.create(order=order, product=product,
                    quantity=qty, unit_price=product.price, subtotal=subtotal)
                total += subtotal
        order.total_amount = total
        order.save()
        return redirect("order_detail", order_id=order.id)
    return render(request, "new_visit.html", {"products":products})

def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related("shop","salesman"), id=order_id)
    return render(request, "order_detail.html", {"order":order})

def whatsapp(request, order_id):
    order = get_object_or_404(Order.objects.select_related("shop","salesman"), id=order_id)
    lines = [
        "🌸 *kavan patel - ORDER SUMMARY*",
        f"Shop: {order.shop.name}",
        f"Owner: {order.shop.owner_name}",
        f"Phone: {order.shop.phone}",
        f"Salesman: {order.salesman.username if order.salesman else 'N/A'}",
        f"Date: {order.order_date.strftime('%d-%m-%Y %I:%M %p')}",
        "",
        "*ORDER:*"
    ]
    for item in order.items.select_related("product"):
        lines.append(f"{item.product.name} x {item.quantity} = ₹{item.subtotal}")
    lines += ["", f"Total: ₹{order.total_amount}", f"Paid: ₹{order.paid_amount}",
              f"Pending: ₹{order.pending_amount}", "", "Thank you - kavan patel"]
    url = "https://wa.me/?text=" + quote("\n".join(lines))
    return redirect(url)
