from datetime import date
from django.db.models import Sum, Count
from decimal import Decimal
from django.core.cache import cache

from collections import defaultdict
from employee.models import Attendance, DailtyProduct


class EmployeeSalaryReport:
    """Aggregated employee salary report generation class"""

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._cached_data = None

    def _prepare_report_data(self, force_refresh=False):
        """Fetch and prepare aggregated data in a single query with caching"""

        cache_key = f"salary_report_{self.start_date}_{self.end_date}"
        if not force_refresh:
            self._cached_data = cache.get(cache_key)

        if self._cached_data is not None:
            return self._cached_data

        # 1. Har kunning mahsulot summasini olish
        daily_products = DailtyProduct.objects.filter(
            date__gte=self.start_date,
            date__lte=self.end_date
        ).values('date').annotate(total=Sum('total_amount'))

        daily_products_dict = {d['date']: d['total'] for d in daily_products}

        # 2. Har kun uchun ishlangan soatlarni olish
        daily_attendance = Attendance.objects.filter(
            check_in__date__gte=self.start_date,
            check_in__date__lte=self.end_date,
            worked_hours__gt=0
        ).values('check_in__date', 'employee_id', 'employee__name').annotate(
            total_worked_hours=Sum('worked_hours')
        )

        # 3. Har kun uchun `hourly_rate` hisoblash
        daily_rates = {}
        for day in daily_products_dict:
            total_hours = sum(a['total_worked_hours'] for a in daily_attendance if a['check_in__date'] == day)
            total_products = daily_products_dict[day]
            daily_rates[day] = (total_products / total_hours) if total_hours > 0 else Decimal('0')

        # 4. Ishchilarni va ularning ish haqini hisoblash
        employee_data = defaultdict(lambda: {'total_salary': Decimal('0'), 'total_hours': Decimal('0'), 'work_days': 0})
        for record in daily_attendance:
            work_date = record['check_in__date']
            hourly_rate = daily_rates.get(work_date, Decimal('0'))
            employee_id = record['employee_id']

            employee_data[employee_id]['employee_name'] = record['employee__name']
            employee_data[employee_id]['total_hours'] += record['total_worked_hours']
            employee_data[employee_id]['total_salary'] += record['total_worked_hours'] * hourly_rate
            employee_data[employee_id]['work_days'] += 1

        # Natijani tayyorlash
        report = [
            {
                'employee_id': emp_id,
                'employee_name': data['employee_name'],
                'work_days': data['work_days'],
                'total_hours': float(data['total_hours']),
                'total_salary': float(round(data['total_salary'], 2))
            }
            for emp_id, data in employee_data.items()
        ]

        total_amount = sum(daily_products_dict.values())

        self._cached_data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_products': total_amount,
            'employees': report,
        }
        cache.set(cache_key, self._cached_data, timeout=60)  # Cache for 1 hour

        return self._cached_data

    def generate_report(self, force_refresh=False):
        """Generate comprehensive salary report"""
        cached_data = self._prepare_report_data(force_refresh)
        report_data = cached_data['employees']
        total_amount = cached_data['total_products']

        return {

            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_amount': float(total_amount),
            'employees': report_data
        }
