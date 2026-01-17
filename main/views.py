from django.shortcuts import render, redirect,get_object_or_404
from .models import *


def home(request):
    about = About.objects.first()
    services = Service.objects.all()
    flights = Flight.objects.all().order_by('date')

    if request.method == "POST":
        ContactRequest.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            flight=request.POST.get("flight"),
            message=request.POST.get("message"),
        )
        return redirect("home")

    return render(request, "main/index.html", {
        "about": about,
        "services": services,
        "flights": flights,
    })




def category_list(request):
    categories = Category.objects.all()
    return render(request, 'album.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    photos = category.photos.all()
    return render(request, 'photo_album.html', {'category': category, 'photos': photos})





#ADMIN

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import About, Service, Flight, ContactRequest, Category, Photo


@staff_member_required(login_url='/admin/login/')
def admin_dashboard(request):
    """Asosiy admin panel sahifasi"""
    
    # About bo'limini yangilash
    if request.method == 'POST' and request.POST.get('action') == 'update_about':
        about = About.objects.first()
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            experience_years = request.POST.get('experience_years')
            clients = request.POST.get('clients')
            destinations = request.POST.get('destinations')
            
            if about:
                about.title = title
                about.description = description
                about.experience_years = experience_years
                about.clients = clients
                about.destinations = destinations
                about.save()
            else:
                About.objects.create(
                    title=title,
                    description=description,
                    experience_years=experience_years,
                    clients=clients,
                    destinations=destinations,
                )
            
            messages.success(request, 'Ma\'lumot yangilandi!')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        
        return redirect('admin_dashboard')
    
    # Statistika
    stats = {
        'flights_count': Flight.objects.count(),
        'requests_count': ContactRequest.objects.count(),
        'categories_count': Category.objects.count(),
        'services_count': Service.objects.count(),
    }
    
    # So'nggi ma'lumotlar
    recent_requests = ContactRequest.objects.all().order_by('-created_at')[:5]
    upcoming_flights = Flight.objects.filter(date__gte=timezone.now().date()).order_by('date')[:5]
    
    # Barcha ma'lumotlar
    all_flights = Flight.objects.all().order_by('-date')
    all_categories = Category.objects.all()
    all_services = Service.objects.all()
    about = About.objects.first()
    
    context = {
        'stats': stats,
        'recent_requests': recent_requests,
        'upcoming_flights': upcoming_flights,
        'flights': all_flights,
        'categories': all_categories,
        'services': all_services,
        'about': about,
    }
    
    return render(request, 'admin/dashboard.html', context)


# ============== PARVOZLAR ==============

@staff_member_required(login_url='/admin/login/')
def manage_flights(request):
    """Barcha parvozlarni ko'rsatish"""
    flights = Flight.objects.all().order_by('-date')
    
    # Pagination
    paginator = Paginator(flights, 10)
    page = request.GET.get('page')
    flights = paginator.get_page(page)
    
    context = {
        'flights': flights,
        'stats': get_stats(),
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required(login_url='/admin/login/')
def add_flight(request):
    """Yangi parvoz qo'shish"""
    if request.method == 'POST':
        try:
            Flight.objects.create(
                from_city=request.POST.get('from_city'),
                to_city=request.POST.get('to_city'),
                date=request.POST.get('date'),
                seats=request.POST.get('seats'),
                price=request.POST.get('price'),
                airline=request.POST.get('airline', ''),
                duration=request.POST.get('duration', ''),
                description=request.POST.get('description', ''),
            )
            messages.success(request, 'Parvoz muvaffaqiyatli qo\'shildi!')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return redirect('admin_dashboard')


@staff_member_required(login_url='/admin/login/')
def edit_flight(request, pk):
    """Parvozni tahrirlash"""
    flight = get_object_or_404(Flight, pk=pk)
    
    if request.method == 'POST':
        try:
            flight.from_city = request.POST.get('from_city')
            flight.to_city = request.POST.get('to_city')
            flight.date = request.POST.get('date')
            flight.seats = request.POST.get('seats')
            flight.price = request.POST.get('price')
            flight.airline = request.POST.get('airline', '')
            flight.duration = request.POST.get('duration', '')
            flight.description = request.POST.get('description', '')
            flight.save()
            
            messages.success(request, 'Parvoz muvaffaqiyatli yangilandi!')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return redirect('admin_dashboard')


@staff_member_required(login_url='/admin/login/')
def delete_flight(request, pk):
    """Parvozni o'chirish"""
    if request.method == 'POST':
        flight = get_object_or_404(Flight, pk=pk)
        flight.delete()
        messages.success(request, 'Parvoz o\'chirildi!')
    
    return redirect('admin_dashboard')


# ============== SO'ROVLAR ==============

@staff_member_required(login_url='/admin/login/')
def manage_requests(request):
    """Barcha so'rovlarni ko'rsatish"""
    contact_requests = ContactRequest.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(contact_requests, 15)
    page = request.GET.get('page')
    contact_requests = paginator.get_page(page)
    
    context = {
        'contact_requests': contact_requests,
        'stats': get_stats(),
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required(login_url='/admin/login/')
def delete_request(request, pk):
    """So'rovni o'chirish"""
    if request.method == 'POST':
        contact_request = get_object_or_404(ContactRequest, pk=pk)
        contact_request.delete()
        messages.success(request, 'So\'rov o\'chirildi!')
    
    return redirect('admin_dashboard')


# ============== KATEGORIYALAR ==============

@staff_member_required(login_url='/admin/login/')
def manage_categories(request):
    """Kategoriyalarni boshqarish"""
    
    # Yangi kategoriya qo'shish
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            cover_image = request.FILES.get('cover_image')
            
            if title and cover_image:
                Category.objects.create(title=title, cover_image=cover_image)
                messages.success(request, 'Kategoriya qo\'shildi!')
            else:
                messages.error(request, 'Barcha maydonlarni to\'ldiring!')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        
        return redirect('admin_dashboard')
    
    # Kategoriyalarni ko'rsatish
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'stats': get_stats(),
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required(login_url='/admin/login/')
def delete_category(request, pk):
    """Kategoriyani o'chirish"""
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Kategoriya o\'chirildi!')
    
    return redirect('admin_dashboard')


# ============== RASMLAR ==============

@staff_member_required(login_url='/admin/login/')
def manage_photos(request, category_id):
    """Kategoriya rasmlarini boshqarish"""
    category = get_object_or_404(Category, pk=category_id)
    
    # Yangi rasm qo'shish
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')
            
            if image:
                Photo.objects.create(category=category, image=image)
                messages.success(request, 'Rasm qo\'shildi!')
            else:
                messages.error(request, 'Rasm tanlang!')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        
        return redirect('manage_photos', category_id=category_id)
    
    # Rasmlarni ko'rsatish
    photos = category.photos.all()
    
    context = {
        'category': category,
        'photos': photos,
        'stats': get_stats(),
    }
    
    return render(request, 'admin/photos.html', context)


@staff_member_required(login_url='/admin/login/')
def delete_photo(request, pk):
    """Rasmni o'chirish"""
    if request.method == 'POST':
        photo = get_object_or_404(Photo, pk=pk)
        category_id = photo.category.id
        photo.delete()
        messages.success(request, 'Rasm o\'chirildi!')
        
        return redirect('manage_photos', category_id=category_id)
    
    return redirect('admin_dashboard')


# ============== XIZMATLAR ==============

@staff_member_required(login_url='/admin/login/')
def manage_services(request):
    """Xizmatlarni boshqarish"""
    
    # Yangi xizmat qo'shish
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            icon = request.POST.get('icon')
            
            if title and description and icon:
                Service.objects.create(
                    title=title,
                    description=description,
                    icon=icon
                )
                messages.success(request, 'Xizmat qo\'shildi!')
            else:
                messages.error(request, 'Barcha maydonlarni to\'ldiring!')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
        
        return redirect('admin_dashboard')
    
    # Xizmatlarni ko'rsatish
    services = Service.objects.all()
    
    context = {
        'services': services,
        'stats': get_stats(),
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required(login_url='/admin/login/')
def delete_service(request, pk):
    """Xizmatni o'chirish"""
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        messages.success(request, 'Xizmat o\'chirildi!')
    
    return redirect('admin_dashboard')


# ============== BIZ HAQIMIZDA ==============

@staff_member_required(login_url='/admin/login/')
def manage_about(request):
    """About bo'limini boshqarish - bu funksiya endi kerak emas, lekin URL uchun qoldirilgan"""
    return redirect('admin_dashboard')


# ============== HELPER FUNCTIONS ==============

def get_stats():
    """Statistika olish uchun yordamchi funksiya"""
    return {
        'flights_count': Flight.objects.count(),
        'requests_count': ContactRequest.objects.count(),
        'categories_count': Category.objects.count(),
        'services_count': Service.objects.count(),
    }
    
def director_view(request):
    return render(request, "main/direktor.html")