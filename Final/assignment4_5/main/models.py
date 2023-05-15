from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    cover_image = models.ImageField(upload_to='images/product/cover_image')
    title = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    price = models.IntegerField()
    country = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    description = models.TextField()
    is_visible = models.BooleanField(default=False)
    id=models.AutoField(primary_key=True)
    def __str__(self):
        return f'{self.title} ({self.model})'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'




class ViewedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_date']

    def __str__(self):
        return f'User: {self.user} <---> Product: {self.product})'



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity