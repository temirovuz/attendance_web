from datetime import datetime

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET


from employee.forms import (
    BreakTimeEmployeeForm,
    CheckInForm,
    CheckOutForm,
    CheckingListForm,
    EmployeeForm,
    ProductForm,
    ProductDailyForm,
    ProductDailySelect,
    SalaryForm,
)
from employee.models import Attendance, DailtyProduct, Employee, Product
from employee.reports import EmployeeSalaryReport

# -----------------------------------------  Employee Views   ----------------------------------------- #


class CreateEmployee(View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, "employee/create_employee.html", {"form": form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("employee_list")
        return render(request, "employee/create_employee.html", {"form": form})


class EmployeeList(View):
    def get(self, request):
        employees = Employee.objects.all()
        return render(request, "employee/employee_list.html", {"employees": employees})


# -----------------------------------------  Employee Update and Delete Views   ----------------------------------------- #
class EmployeeUpdateDeleteView(View):
    def get(self, request, pk):
        """Xodimni tahrirlash uchun forma ko‘rsatish"""
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeForm(instance=employee)
        return render(
            request, "employee/employee_edit.html", {"form": form, "employee": employee}
        )

    def post(self, request, pk):
        """Xodimni yangilash yoki o‘chirish"""
        employee = get_object_or_404(Employee, pk=pk)

        if "delete" in request.POST:  # Agar delete tugmasi bosilgan bo‘lsa
            employee.delete()
            return redirect("employee_list")

        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(
                "employee_list"
            )  # Ma'lumot yangilangandan keyin qayta yo‘naltirish
        return render(
            request, "employee/employee_edit.html", {"form": form, "employee": employee}
        )


# -----------------------------------------  Product Views   ----------------------------------------- #


class ProductCreate(View):
    def get(self, request):
        form = ProductForm()
        return render(request, "product/create_product.html", {"form": form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
        return render(request, "product/create_product.html", {"form": form})


class ProductList(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, "product/product_list.html", {"products": products})


# -------------------------------------------  Product Update and Delete Views   ----------------------------------------- #


class ProductUpdateDeleteView(View):
    def get(self, request, pk):
        """Mahsulotni tahrirlash uchun forma ko‘rsatish"""
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(
            request, "product/product_edit.html", {"form": form, "product": product}
        )

    def post(self, request, pk):
        """Mahsulotni yangilash yoki o‘chirish"""
        product = get_object_or_404(Product, pk=pk)

        if "delete" in request.POST:  # Agar delete tugmasi bosilgan bo‘lsa
            product.delete()
            return redirect("product_list")

        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(
                "product_list"
            )  # Ma'lumot yangilangandan keyin qayta yo‘naltirish
        return render(
            request, "product/product_edit.html", {"form": form, "product": product}
        )


# -----------------------------------------  Product Daily Views   ----------------------------------------- #


class ProductDailyCreate(View):
    def get(self, request):
        product = Product.objects.all()
        form = ProductDailyForm()
        return render(
            request,
            "product/create_product_daily.html",
            {"form": form, "products": product},
        )

    def post(self, request):
        form = ProductDailyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_daily_list")
        return render(request, "product/create_product_daily.html", {"form": form})


class ProductDailyList(View):
    def get(self, request):
        form = ProductDailySelect()
        return render(request, "product/product_daily_list.html", {"form": form})

    def post(self, request):
        form = ProductDailySelect(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            product_dailys = DailtyProduct.objects.filter(
                date__range=(start_date, end_date)
            )
            return render(
                request,
                "product/product_daily_list.html",
                {"form": form, "product_dailys": product_dailys},
            )
        return render(request, "product/product_daily_list.html", {"form": form})

    def delete(self, request, pk):
        product_daily = DailtyProduct.objects.get(pk=pk)
        product_daily.delete()
        return JsonResponse(
            {"status": "success", "message": "Product Daily deleted successfully."}
        )


# -----------------------------------------  Product Daily Update and Delete Views   ----------------------------------------- #


class ProductDailyUpdateDeleteView(View):
    def get(self, request, pk):
        """Mahsulotni tahrirlash uchun forma ko‘rsatish"""
        product_daily = get_object_or_404(DailtyProduct, pk=pk)
        form = ProductDailyForm(instance=product_daily)
        return render(
            request,
            "product/product_daily_edit.html",
            {"form": form, "product_daily": product_daily},
        )

    def post(self, request, pk):
        """Mahsulotni yangilash yoki o‘chirish"""
        product_daily = get_object_or_404(DailtyProduct, pk=pk)

        if "delete" in request.POST:  # Agar delete tugmasi bosilgan bo‘lsa
            product_daily.delete()
            return redirect("product_daily_list")

        form = ProductDailyForm(request.POST, instance=product_daily)
        if form.is_valid():
            form.save()
            return redirect(
                "product_daily_list"
            )  # Ma'lumot yangilangandan keyin qayta yo‘naltirish
        return render(
            request,
            "product/product_daily_edit.html",
            {"form": form, "product_daily": product_daily},
        )


# -----------------------------------------  Check In and Check Out Views   ----------------------------------------- #


class CheckInView(View):
    def get(self, request):
        queryset = Employee.objects.exclude(attendances__check_out__isnull=True)
        form = CheckInForm()
        return render(
            request, "attendance/check_in.html", {"form": form, "employees": queryset}
        )

    def post(self, request):
        form = CheckInForm(request.POST)
        if form.is_valid():
            employees = form.cleaned_data.get("employees").values_list("id", flat=True)
            check_in_time = form.cleaned_data.get("check_in")
            for employee in employees:
                if isinstance(employee, Employee):
                    employee.attendances.create(check_in=check_in_time)
                else:
                    employee_obj = Employee.objects.get(id=employee)
                    employee_obj.attendances.create(check_in=check_in_time)
            return redirect("home")
        return render(request, "attendance/check_in.html", {"form": form})


class CheckOutView(View):
    def get(self, request):
        queryset = Attendance.objects.filter(check_out__isnull=True)
        form = CheckOutForm()
        print(queryset)
        return render(
            request, "attendance/check_out.html", {"form": form, "employees": queryset}
        )

    def post(self, request):
        form = CheckOutForm(request.POST)
        print(form.data)
        print(form.is_valid())
        if form.is_valid():
            employees = form.cleaned_data.get("employees").values_list("id", flat=True)
            check_out = form.cleaned_data.get("check_out")
            for employee_id in employees:
                attendance = Attendance.objects.filter(
                    id=employee_id, check_out__isnull=True
                ).first()
                if attendance:
                    attendance.check_out = check_out
                    attendance.save()
            return redirect("home")
        return render(request, "attendance/check_out.html", {"form": form})


# -------------------------------------     View attendance for a specific day  ----------------------------------------------- #


class AttendanceView(View):
    def get(self, request):
        form = CheckingListForm()
        return render(request, "attendance/checking_list.html", {"form": form})

    def post(self, request):
        form = CheckingListForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            attendances = Attendance.objects.filter(check_in__date=date)
            return render(
                request,
                "attendance/checking_list.html",
                {"form": form, "attendances": attendances},
            )


# ----------------------------------- calculating the wages of employees for given days ------------------------------------- #


class SalaryComputationView(View):
    def get(self, request):
        form = SalaryForm()
        return render(request, "salary/salary _computation.html", {"form": form})

    def post(self, request):
        form = SalaryForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            cache_key = f"salary_report_{start_date}_{end_date}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return render(
                    request=request,
                    template_name="salary/salary_list.html",
                    context={"form": form, "informations": cached_data},
                )

            report_instance = EmployeeSalaryReport(start_date, end_date)
            report_data = report_instance.generate_report()

            cache.set(cache_key, report_data, timeout=180)
            print(report_data)

            return render(
                request=request,
                template_name="salary/salary_list.html",
                context={"form": form, "informations": report_data},
            )


# -----------------------------------------  employee taking a temporary leave of absence from work  ----------------------------------------- #


class EmployeeSearchView(View):
    @method_decorator(require_GET)
    def get(self, request):
        print("kirdi")
        # Agar bu AJAX yoki fetch so‘rovi bo‘lsa
        if request.headers.get(
            "x-requested-with"
        ) == "XMLHttpRequest" or request.GET.get("name"):
            name_query = request.GET.get("name", "").strip()
            print("kirdi")
            if name_query:
                employees = Employee.objects.filter(name__icontains=name_query)
                data = {
                    "employees": [
                        {
                            "id": emp.id,
                            "name": emp.name,
                            "status": emp.get_status_display(),
                            "full_info": str(emp),
                        }
                        for emp in employees
                    ]
                }
            else:
                data = {"employees": []}
            return JsonResponse(data)

        # Aks holda, oddiy HTML sahifa render qilinadi
        return render(request, "attendance/search_employee.html")

    def post(self, request):
        employee_id = request.POST.get("employee_id")
        date_str = request.POST.get("date")

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Sana noto‘g‘ri formatda", status=400)

        employee_yes = Attendance.objects.filter(
            employee=employee_id, check_in__date=date_obj
        ).first()
        if employee_yes:
            request.session["employee_id"] = employee_id
            request.session["date"] = date_obj.isoformat()
            return redirect("breaktime")
        else:
            return HttpResponse(
                f"<h1>Ushbu ishchi {date_obj} sanada ishga kelmagan! Xato malumot kiritmang iltimos.</h1>"
            )


class BrakingTimeView(View):
    def get(self, request):
        form = BreakTimeEmployeeForm()
        return render(request, "attendance/break_time.html", {"form": form})
    
    def post(self, request):
        form = BreakTimeEmployeeForm(request.POST)
        if form.is_valid():
            # Process the form data here
            break_time = form.cleaned_data.get("break_time")
            employee = Attendance.objects.get(
                employee=request.session["employee_id"],
                check_in__date=request.session["date"],
            )
            if employee:
                employee.break_time = break_time
                employee.save()
            return redirect("home")
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)
