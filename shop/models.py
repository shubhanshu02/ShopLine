from django.db import models

class Seller(models.Model):
    name = models.CharField(null=False, max_length=200)
    contactNumber = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Item(models.Model):
    name = models.CharField(null=False, max_length=200)
    price = models.IntegerField(null=False)
    quantities_available = models.IntegerField(null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'price']


class BillItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total = models.IntegerField()


class Bill(models.Model):
    customer = models.CharField(max_length=100)
    dateTime = models.DateTimeField()
    total = models.IntegerField()
    items = models.ManyToManyField(BillItem)
