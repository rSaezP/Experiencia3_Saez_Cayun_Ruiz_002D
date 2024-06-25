from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .models import Cliente, DetalleCompra, Compra, BoletaCompra
from .forms import ProductoForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

# Create your views here.

def inicio(request):
    context={}
    return render(request, 'boutique_noemi/inicio.html', context)

def galeria(request):
    context={}
    return render(request, 'boutique_noemi/galeria.html', context)

def quienes_somos(request):
    context={}
    return render(request, 'boutique_noemi/quienes_somos.html', context)

def contacto(request):
    context={}
    return render(request, 'boutique_noemi/contacto.html', context)

def suscribir(request):
    context={}
    return render(request, 'boutique_noemi/suscribir.html', context)

def calculadora_tallas(request):
    context={}
    return render(request, 'boutique_noemi/calculadora_tallas.html', context)


def es_administrador(user):
    return user.is_authenticated and user.es_administrador

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                producto = form.save(commit=False)
                
                if producto.precio <= 0:
                    raise ValidationError("El precio debe ser mayor que cero.")
                if producto.stock < 0:
                    raise ValidationError("El stock no puede ser negativo.")
                producto.save()
                return redirect('lista_productos')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ProductoForm()
    return render(request, 'boutique_noemi/crear_producto.html', {'form': form})

@user_passes_test(es_administrador)
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'boutique_noemi/actualizar_producto.html', {'form': form, 'producto': producto})

@user_passes_test(es_administrador)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'boutique_noemi/eliminar_producto.html', {'producto': producto})

def realizar_compra(request, producto_id):
    carrito = get_object_or_404(Compra, cliente=request.user.cliente, estado='en_proceso')
    if carrito.detallecompra_set.exists():
        for detalle in carrito.detallecompra_set.all():
            if detalle.producto.stock < detalle.cantidad:
                messages.error(request, f"No hay suficiente stock de {detalle.producto.nombre}")
                return redirect('carrito')
            detalle.producto.stock -= detalle.cantidad
            detalle.producto.save()
        carrito.estado = 'completada'
        carrito.save()
        messages.success(request, "Compra realizada con éxito")
        return redirect('compra_exitosa')
    else:
        messages.error(request, "Tu carrito está vacío")
        return redirect('carrito')

@login_required
def lista_productos(request):
    productos = Producto.objects.all().order_by('-fecha_modificacion')
    paginator = Paginator(productos, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'boutique_noemi/lista_productos.html', {'page_obj': page_obj})




@login_required
def carrito(request):
    carrito, created = Compra.objects.get_or_create(cliente=request.user, estado='en_proceso')
    productos = carrito.detallecompra_set.all().annotate(
        total=F('cantidad') * F('producto__precio')
    )
    total = productos.aggregate(total=Sum('total'))['total'] or 0
    return render(request, 'boutique_noemi/carrito.html', {
        'productos': productos,
        'total': total
    })

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Compra.objects.get_or_create(cliente=request.user.cliente, estado='en_proceso')
    detalle, created = DetalleCompra.objects.get_or_create(compra=carrito, producto=producto)
    if not created:
        detalle.cantidad += 1
    else:
        detalle.cantidad = 1
    detalle.save()
    messages.success(request, f"{producto.nombre} añadido al carrito.")
    return redirect('carrito')

@login_required
def cambiar_cantidad_carrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = Compra.objects.get(cliente=request.user.cliente, estado='en_proceso')
        detalle = get_object_or_404(DetalleCompra, compra=carrito, producto=producto)
        detalle.cantidad = cantidad
        detalle.save()
    return redirect('carrito')

@login_required
def eliminar_producto_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = Compra.objects.get(cliente=request.user.cliente, estado='en_proceso')
        DetalleCompra.objects.filter(compra=carrito, producto=producto).delete()
    return redirect('carrito')

@login_required
def procesar_carrito(request):
    carrito = get_object_or_404(Compra, cliente=request.user.cliente, estado='en_proceso')
    if carrito.detallecompra_set.exists():
        for detalle in carrito.detallecompra_set.all():
            if detalle.producto.stock < detalle.cantidad:
                messages.error(request, f"No hay suficiente stock de {detalle.producto.nombre}")
                return redirect('carrito')
            detalle.producto.stock -= detalle.cantidad
            detalle.producto.save()
        carrito.estado = 'completada'
        carrito.save()
        messages.success(request, "Compra realizada con éxito")
        return redirect('compra_exitosa')
    else:
        messages.error(request, "Tu carrito está vacío")
        return redirect('carrito')
    
def ver_carrito(request):
    carrito, created = Compra.objects.get_or_create(cliente=request.user.cliente, estado='en_proceso')
    productos = carrito.detallecompra_set.all().annotate(
        total=F('cantidad') * F('producto__precio')
    )
    total = productos.aggregate(total=Sum('total'))['total'] or 0
    return render(request, 'boutique_noemi/carrito.html', {
        'productos': productos,
        'total': total
    })

@login_required
def compra_exitosa(request):
    return render(request, 'boutique_noemi/compra_exitosa.html')