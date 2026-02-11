from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.utils.html import format_html
from datetime import date
import pandas as pd

from .models import Trainee, Department, User, Registration
from .serializers import TraineeImportSerializer


admin.site.register(Department)
admin.site.register(Registration)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('معلومات الموظف', {'fields': ('department',)}),)



class CsvImportForm(forms.Form):
    excel_file = forms.FileField(label="اختر ملف الإكسل (.xlsx)")



@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):

    list_display = ('trainee_id', 'name', 'phone', 'department', 'paid', 'end_date', 'status_colored')

    list_filter = ('department', 'paid', 'end_date')
    search_fields = ('name', 'phone', 'trainee_id')
    change_list_template = "admin/trainees_changelist.html"

    def status_colored(self, obj):
        if not obj.end_date: return "-"
        days = (obj.end_date - date.today()).days
        if days < 0:
            color, bg = "red", "#ffe6e6"
            msg = f"منتهي ({abs(days)})"
        elif days <= 7:
            color, bg = "#b35900", "#fff3cd"
            msg = f"قريب ({days})"
        else:
            color, bg = "green", "#e6fffa"
            msg = f"نشط ({days})"
        return format_html(
            '<span style="color:{};background:{};padding:3px 10px;border-radius:15px;font-weight:bold;">{}</span>',
            color, bg, msg)

    status_colored.short_description = "الحالة"


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs
        if request.user.department: return qs.filter(department=request.user.department)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.department_id:
            obj.department = request.user.department
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['department'].disabled = True
            form.base_fields['department'].initial = request.user.department
        return form

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('import-excel/', self.import_excel), ]
        return my_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]
            try:
                df = pd.read_excel(excel_file)
                df.columns = df.columns.str.strip()

                rename_map = {
                    'Name': 'name', 'name': 'name',
                    'ID': 'trainee_id', 'Id': 'trainee_id', 'id': 'trainee_id',
                    'MOBILE No.': 'phone', 'MBile No.': 'phone', 'Mobile': 'phone', 'Phone': 'phone', 'phone': 'phone',
                    'SPECALITY': 'speciality', 'Speciality': 'speciality', 'speciality': 'speciality', 'spec': 'speciality',
                    'Starting DATE': 'start_date', 'Starting Date': 'start_date',
                    'Ending Date': 'end_date', 'Ending date': 'end_date',
                    'Paid': 'paid', 'paid': 'paid',
                    'Group': 'group', 'group': 'group',
                    'Note': 'note', 'note': 'note',
                    'Department': 'department_name'
                }

                df = df.rename(columns=rename_map)
                success_count, errors = 0, []

                for index, row in df.iterrows():
                    s_date = pd.to_datetime(row.get('start_date')).date() if pd.notnull(row.get('start_date')) else None
                    e_date = pd.to_datetime(row.get('end_date')).date() if pd.notnull(row.get('end_date')) else None

                    paid_val = row.get('paid')
                    if isinstance(paid_val, str): paid_val = paid_val.strip().title()

                    if request.user.is_superuser:
                        dept_name = row.get('department_name', 'General')
                    else:
                        dept_name = request.user.department.name if request.user.department else 'General'

                    data = {
                        "trainee_id": row.get('trainee_id'),
                        "name": row.get('name'),
                        "phone": row.get('phone'),
                        "speciality": row.get('speciality'),
                        "start_date": s_date,
                        "end_date": e_date,
                        "paid": paid_val,
                        "group": row.get('group'),
                        "note": row.get('note', '') if pd.notnull(row.get('note')) else '',
                        "department_name": dept_name
                    }

                    serializer = TraineeImportSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        success_count += 1
                    else:
                        errors.append(f"سطر {index + 2}: {serializer.errors}")

                if success_count > 0: messages.success(request, f"تم استيراد {success_count} متدرب.")
                if errors: messages.warning(request, f"أخطاء: {errors[:2]}")

            except Exception as e:
                messages.error(request, f"خطأ: {e}")
            return redirect("..")

        form = CsvImportForm()
        return render(request, "admin/excel_form.html", {"form": form})

admin.site.site_header = "نظام إدارة المتدربين"

admin.site.site_title = "نظام المتدربين"

admin.site.index_title = "لوحة تحكم المشرفين"