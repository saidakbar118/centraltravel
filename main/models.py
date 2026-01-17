from django.db import models


class About(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    experience_years = models.PositiveIntegerField(default=0)
    clients = models.PositiveIntegerField(default=0)
    destinations = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class (masalan: fas fa-kaaba)"
    )

    def __str__(self):
        return self.title



class Flight(models.Model):
    from_city = models.CharField(max_length=100, verbose_name="Qayerdan")
    to_city = models.CharField(max_length=100, verbose_name="Qayerga")
    date = models.DateField(verbose_name="Sana")
    seats = models.PositiveIntegerField(verbose_name="Qolgan joylar")
    price = models.CharField(max_length=50, verbose_name="Narx")  # yoki DecimalField agar faqat raqam bo'lsa
    airline = models.CharField(max_length=100, verbose_name="Aviakompaniya", blank=True, null=True)
    duration = models.CharField(max_length=50, verbose_name="Parvoz vaqti", blank=True, null=True)
    description = models.TextField(verbose_name="Qo'shimcha ma'lumot", blank=True, null=True)

    def __str__(self):
        return f"{self.from_city} → {self.to_city} ({self.date})"
    
    class Meta:
        verbose_name = "Parvoz"
        verbose_name_plural = "Parvozlar"
        ordering = ['date']



class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    flight = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='album/')

    def __str__(self):
        return f"Category {self.id}"


class Photo(models.Model):
    category = models.ForeignKey(Category, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='album/')

    def __str__(self):
        return f"Photo {self.id} (Category {self.category.id})"
