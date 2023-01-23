from django.db import models

# Create your models here.
# vendor
class Vendor(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="vendor/")
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    status  = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '1. Vendors'

    
    def __str__(self) -> str:
        return self.full_name




# unit
class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '2. Units'

    
    def __str__(self) -> str:
        return self.title





# product
class Product(models.Model):
    title = models.CharField(max_length=255)
    deatail = models.TextField()

    unit = models.ForeignKey(Unit, on_delete= models.CASCADE )
    photo = models.ImageField(upload_to="product/")
    
    class Meta:
        verbose_name_plural = '3. Products'

    def __str__(self) -> str:
        return self.title



# purchase
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE  )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE )
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False, default=0)
    purchace_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '4. Purchases'

    def save(self, *args, **kwargs ):
        self.total_amount = self.quantity*self.price
        super(Purchase, self ).save(*args, **kwargs)

        # inventory effect 
        inventory = Inventory.objects.filter(product = self.product).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_balance_quantity = self.quantity
        else:
            totalBal = self.quantity
        
        Inventory.objects.create(
            product = self.product,
            purchase = self,
            sale = None,
            purchase_quantity = self.quantity,
            sales_quantity = None,
            total_balance_quantity  = totalBal
        )

# customer  
class Customer(models.Model):
    customer_name = models.CharField(max_length=255, blank=True   )
    customer_mobile  = models.CharField(max_length=15)
    customer_address = models.CharField(max_length=50, blank=True, null= True  )

    class Meta:
        verbose_name_plural= '7. Customers'



    def __str__(self) -> str:
        return self.customer_name

    




# sales
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True )
    quantity = models.FloatField()
    price = models.FloatField()
    total_amount = models.FloatField(editable=False)
    sales_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "5. Sales"
    


  

    def save(self, *args, **kwargs ):
        self.total_amount = self.quantity*self.price
        super(Sale, self ).save(*args, **kwargs)

        # inventory effect 
        inventory = Inventory.objects.filter(product = self.product).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_balance_quantity - self.quantity
       
        Inventory.objects.create(
            product = self.product,
            purchase = None,
            sale = self,
            purchase_quantity =None,
            sales_quantity = self.quantity,
            total_balance_quantity  = totalBal
        )





# inventory
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default=0, null=True   )
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default=0 , null=True    )    
    purchase_quantity = models.FloatField(default=0, null=True)
    sales_quantity = models.FloatField(default=0, null=True)
    total_balance_quantity = models.FloatField()

    class Meta:
        verbose_name_plural = "6. Inventory"

    def __str__(self) -> str: 
        return self.product
    
    def product_unit(self):
        return self.product.unit.title



    def purchase_date(self):
        if self.purchase:
            return self.purchase.purchace_date
    
    def sale_date(self):
        if self.sale:
            return self.sale.sales_date


