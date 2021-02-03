from django import forms
from .models import Project, Me
# from django.contrib.auth.models import User 

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['title','description','url','project_image','software_used']
		widgets = {
			'description':forms.Textarea
		}
		
class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = Me
		fields = ["profile_pic", "background_pic", "about_me"]

