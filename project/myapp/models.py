from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    student_class = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class FeeStructure(models.Model):
    TERM_CHOICES = [('Term 1', 'Term 1'), ('Term 2', 'Term 2'), ('Term 3', 'Term 3')]
    FEE_TYPE_CHOICES = [('Tuition', 'Tuition'), ('Exam', 'Exam'), ('Development', 'Development'), ('Other', 'Other')]

    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.term} - {self.fee_type}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [('Cash', 'Cash'), ('EcoCash', 'EcoCash'), ('Bank Transfer', 'Bank Transfer'), ('Swipe', 'Swipe')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    fee_type = models.CharField(max_length=20, default='Tuition')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    receipt_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.receipt_number} by {self.student}"


class Owing(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.student} owes {self.amount_owed}"
