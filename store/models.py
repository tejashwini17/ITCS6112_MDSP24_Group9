from django.db import models
from django.contrib.auth.models import User


# Create your models here.w
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, related_name='customer', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default="user.jpg")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    CATEGORY = (
        ('VEG', 'VEG'),
        ('NON-VEG', 'NON-VEG'),
        ('SNACKS', 'SNACKS'),
    )
    AVA = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=500, null=True)
    image = models.ImageField(null=True, blank=True)
    available = models.CharField(max_length=200, null=True, choices=AVA, default=AVA[0][0])

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    status = models.CharField(max_length=200, null=True, choices=STATUS, default=STATUS[0][0])

    def __str__(self):
        return str(self.id)

    @property
    def delivery(self):
        delivery = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.order_type == "HOME DELIVERY":
                delivery = True
        return delivery

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    ORDER_TYPE = (
        ('HOME DELIVERY', 'HOME DELIVERY'),
        ('DINE IN', 'DINE IN'),

    )
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    order_type = models.CharField(max_length=100, null=True, blank=True, choices=ORDER_TYPE, default=ORDER_TYPE[0][0])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item)

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total


class DeliveryInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
