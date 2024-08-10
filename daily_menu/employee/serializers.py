from datetime import date

from rest_framework import serializers

from .models import Employee, EmployeeVote


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'name', 'surname']


class EmployeeVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeVote
        fields = ['employee', 'menu']

    def validate(self, data):
        validated_data = super().validate(data)
        
        employee = validated_data.get('employee')
        already_voted = EmployeeVote.objects.filter(employee=employee, voted_at=date.today())
        
        if already_voted:
            raise serializers.ValidationError('Employee has already voted for todays menu')
        return validated_data
