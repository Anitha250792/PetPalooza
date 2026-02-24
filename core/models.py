from django.db import models


class HeroSlide(models.Model):
      title = models.CharField(max_length=200)
      image = models.ImageField(upload_to='hero/')
      is_active = models.BooleanField(default=True)

      def __str__(self):
        return self.title


class PetCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="pets/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PromoSection(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="promo/")

    def __str__(self):
        return self.title


class ServiceCard(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="services/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title