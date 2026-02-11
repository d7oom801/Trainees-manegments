from rest_framework import serializers
from .models import Trainee, Department, Registration


class TraineeImportSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    trainee_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Trainee
        fields = ['trainee_id','name', 'phone', 'speciality', 'start_date', 'end_date', 'paid', 'group', 'note', 'department_name']


    def validate_phone(self, value):
        s_val = str(value).strip().lower()

        empty_values = ['', 'nan', 'none', 'null', '0', '0.0']

        if value is None or s_val in empty_values:
            return ""

        s_val_clean = str(value).strip()

        if s_val_clean.startswith('5'):
            s_val_clean = '0' + s_val_clean

        if not s_val_clean.startswith('05'):
            raise serializers.ValidationError("رقم الجوال يجب أن يبدأ بـ 05")

        return s_val_clean

    def create(self, validated_data):
        dept_name = validated_data.pop('department_name', 'General')
        department, _ = Department.objects.get_or_create(name=dept_name)
        trainee = Trainee.objects.create(department=department, **validated_data)
        return trainee

class registrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'