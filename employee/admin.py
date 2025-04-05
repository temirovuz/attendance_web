from django.contrib import admin

from employee.models import Attendance, DailtyProduct, Employee, Product, Salary


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = ("name", "status")
    list_display = ("id", "name", "status")
    list_filter = ("status",)
    search_fields = ("name",)
    ordering = ("id",)
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ("name", "price_per_unit")
    list_display = ("id", "name", "price_per_unit")
    search_fields = ("name",)
    ordering = ("id",)
    list_per_page = 20


@admin.register(DailtyProduct)
class DailtyProductAdmin(admin.ModelAdmin):
    fields = ("date", "product", "quantity")
    list_display = ("id", "date", "product", "quantity", "total_amount")
    search_fields = ("product__name",)
    ordering = ("id",)
    list_per_page = 20


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    fields = ("employee", "check_in", "check_out")
    list_display = ("id", "employee", "check_in", "check_out", "worked_hours", "break_time")
    search_fields = ("employee__name",)
    ordering = ("id",)
    list_per_page = 20


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    fields = ("start_date", "end_date", "amount")
    list_display = ("id", "start_date", "end_date", "amount")
    search_fields = ("employee__name",)
    ordering = ("id",)
    list_per_page = 20
