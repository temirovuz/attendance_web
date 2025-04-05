from django.db import models


class Employee(models.Model):
    CHOICES_STATUS = [("yangi", "Yangi"), ("doimiy", "Doimiy"), ("bolalar", "Bolalar")]
    status = models.CharField(max_length=25, choices=CHOICES_STATUS, default="yangi")
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
    
    def __str__(self):
        return self.name + " " + self.status


class Product(models.Model):
    name = models.CharField(max_length=155)
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["id"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class DailtyProduct(models.Model):
    date = models.DateField()
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=False
    )
    quantity = models.BigIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["id"]
        verbose_name = "Daily Product"
        verbose_name_plural = "Daily Products"

    def save(self, *args, **kwargs):
        if self.product:
            product = Product.objects.filter(id=self.product.id).first()
            if product:
                self.total_amount = self.quantity * product.price_per_unit
        super().save(*args, **kwargs)

        def __str__(self):
            return f"{self.date} - {self.product.name} - {self.quantity} - {self.total_amount}"


class Attendance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="attendances",
    )
    check_in = models.DateTimeField(db_index=True)
    check_out = models.DateTimeField(db_index=True, null=True, blank=True)
    worked_hours = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    break_time = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, default=0.0
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"
        indexes = [
            models.Index(fields=["check_in"]),
            models.Index(fields=["check_out"]),
        ]

    def __str__(self):
        return f"{self.employee} - {self.check_in.strftime('%Y-%m-%d %H:%M:%S')}"

    def save(self, *args, **kwargs):
        if self.check_out:
            duration = (self.check_out - self.check_in).total_seconds() / 3600
            self.worked_hours = round(duration - float(self.break_time or 0), 2)
        super().save(*args, **kwargs)


class Salary(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["start_date", "end_date"],
                name="unique_salary_period",
            )
        ]
        verbose_name = "Salary"
        verbose_name_plural = "Salaries"

    def __str__(self):
        return f"{self.amount} - {self.date}"
