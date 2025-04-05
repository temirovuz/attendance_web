from django.utils import timezone
from django import forms
from employee.models import Attendance, Employee, Product, DailtyProduct


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "status"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price_per_unit"]


class ProductDailyForm(forms.ModelForm):
    class Meta:
        model = DailtyProduct
        fields = ["product", "date", "quantity"]


class ProductDailySelect(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="End Date"
    )


class CheckInForm(forms.Form):
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.exclude(
            attendances__check_in__date=timezone.now().date(),
            attendances__check_out__isnull=True,
        ),
        widget=forms.CheckboxSelectMultiple,
        label="employees",
    )
    check_in = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Check In",
        help_text="Enter the check-in time",
    )


class CheckOutForm(forms.Form):
    check_out = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        initial=timezone.now,
        label="Check Out",
        help_text="Enter the check-out time",
    )

    employees = forms.ModelMultipleChoiceField(
        queryset=Attendance.objects.filter(check_out__isnull=True),
        widget=forms.CheckboxSelectMultiple,
        label="employees",
    )
   

class CheckingListForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Start Date"
    )


class SalaryForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="End Date"
    )
    submit = forms.CharField(
        widget=forms.TextInput(attrs={"type": "submit", "value": "Submit"}),
        required=False,
        label="",
    )


class BreakTimeEmployeeForm(forms.Form):
    break_time = forms.DecimalField(
        widget=forms.NumberInput(attrs={"step": "0.01"}), label="Break Time (in hours)"
    )
