from django.urls import path

from employee.views import (
    AttendanceView,
    BrakingTimeView,
    CheckInView,
    CheckOutView,
    CreateEmployee,
    EmployeeList,
    EmployeeSearchView,
    EmployeeUpdateDeleteView,
    ProductDailyUpdateDeleteView,
    ProductList,
    ProductCreate,
    ProductDailyCreate,
    ProductDailyList,
    ProductUpdateDeleteView,
    SalaryComputationView,
)


urlpatterns = [
    path("employee/create/", CreateEmployee.as_view(), name="create_employee"),
    path("employees/", EmployeeList.as_view(), name="employee_list"),
    path(
        "employee/<int:pk>/", EmployeeUpdateDeleteView.as_view(), name="employee_edit"
    ),
    # -----------------------------------------  Product Views   ----------------------------------------- #
    path("product/create/", ProductCreate.as_view(), name="create_product"),
    path("products/", ProductList.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductUpdateDeleteView.as_view(), name="product_edit"),
    # -----------------------------------------  Product Daily Views   ----------------------------------------- #
    path(
        "product_daily/create/",
        ProductDailyCreate.as_view(),
        name="create_product_daily",
    ),
    path("product_dailys/", ProductDailyList.as_view(), name="product_daily_list"),
    path(
        "product_daily/<int:pk>/",
        ProductDailyUpdateDeleteView.as_view(),
        name="product_daily_edit",
    ),
    # -----------------------------------------  Attendance Views   ----------------------------------------- #
    path("checkin/", CheckInView.as_view(), name="checkin"),
    path("checkout/", CheckOutView.as_view(), name="checkout"),
    path("checklist/", AttendanceView.as_view(), name="check_list"),
    # -------------------------------------  Salary Views   ----------------------------------------- #
    path("calculate_salary/", SalaryComputationView.as_view(), name="calculate_salary"),
    # -------------------------------------  Break Time Views   ----------------------------------------- #
    path("search-employee/", EmployeeSearchView.as_view(), name="search_employee"),
    path("breaktime/", BrakingTimeView.as_view(), name="breaktime"),
]
