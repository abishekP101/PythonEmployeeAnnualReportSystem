from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)  # Ensure user is required
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.name

    # Adding a related name for reverse lookup
    @property
    def report(self):
        return self.annualreport_set.first()  # To get the first related AnnualReport


class AnnualReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    duties_description = models.TextField(verbose_name="Brief description of duties", null=True)
    program_description = models.TextField(verbose_name="Brief description about the program/projects/Field study", null=True)
    achievement_description = models.TextField(verbose_name="Your Achievement there to in 100 words", null=True)
    publications_description = models.TextField(verbose_name="Major publications/reports/Technology transferred/patents filed", null=True)
    contribution_description = models.TextField(verbose_name="Specific contribution made to different mission of the Government like Atma Nirbhar Bharat", null=True)
    score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, default="pending", choices=[("pending", "Pending"), ("viewed", "Viewed")])

    def __str__(self):
        return f"Report for {self.employee.name} - {self.year}"
