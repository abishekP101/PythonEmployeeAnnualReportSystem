from django import forms
from .models import Employee, AnnualReport
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','user' , 'job_title', 'department', 'date_of_joining']

    def save(self, commit=True):
        employee = super().save(commit=False)
        if not employee.user:
            employee.user = self.instance.user  # This assumes user is set by the view
        if commit:
            employee.save()
        return employee


class AnnualReportForm(forms.ModelForm):
    class Meta:
        model = AnnualReport
        fields = ['employee', 'year', 'report', 'duties_description', 'program_description',
                  'achievement_description', 'publications_description', 'contribution_description']
        widgets = {
            'report': forms.Textarea(attrs={'rows': 4}),
            'duties_description': forms.Textarea(attrs={'rows': 4}),
            'program_description': forms.Textarea(attrs={'rows': 4}),
            'achievement_description': forms.Textarea(attrs={'rows': 4}),
            'publications_description': forms.Textarea(attrs={'rows': 4}),
            'contribution_description': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        # Automatically assign the logged-in user’s employee to the form
        if not self.instance.employee:
            self.instance.employee = Employee.objects.get(user=self.user)  # Ensure user is set here
        return super().save(commit)


class AnnualReportScoreForm(forms.ModelForm):
    score = forms.IntegerField(min_value=1, max_value=10, label="Score (1-10)")

    class Meta:
        model = AnnualReport
        fields = ['score']

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score < 1 or score > 10:
            raise forms.ValidationError("Please enter a score between 1 and 10.")
        return score