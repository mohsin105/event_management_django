from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group,Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth.forms import AuthenticationForm
User=get_user_model()



class ParticipantModelForm(forms.ModelForm):
    #manually declaring new form fields
    password1=forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter Password',
            'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
        }
    ))
    confirm_password=forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder':'Enter password again',
            'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
        }
    ))

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','profile_image','phone_number','password1','confirm_password'] 
        #by default, only fields that are declared in User model
        # model=Participant
        # fields=['name','email','events']

        # widgets={'events':forms.CheckboxSelectMultiple(attrs={'class':'border border-3'})}
        widgets={
            'username':forms.TextInput(
                attrs={
                    'placeholder':'Username',
                    'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
                }
            ),
            'first_name':forms.TextInput(
                attrs={
                    'placeholder':'First Name',
                    'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
                }
            ),
            'last_name':forms.TextInput(
                attrs={
                    'placeholder':'Last Name',
                    'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'placeholder':'demo@gmail.com',
                    'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
                }
            ),
            'phone_number':forms.TextInput(
                attrs={
                    'placeholder':'Phone Number',
                    'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
                }
            ),
            
        }
    
    # Error validation for field-error
    def clean_password1(self):
        password1=self.cleaned_data.get('password1')
        errors=[]
        if len(password1)<8:
            errors.append("Password is less than 8 char")
        
        # elif re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password1):
        #     raise forms.ValidationError("use proper characters")
        if not re.search(r'[A-Z]',password1):
            errors.append('Password must include at least one uppercase letter.')
        
        if not re.search(r'[a-z]',password1):
            errors.append('Password must include at least one lowercase letter.')
        if not re.search(r'[0-9]',password1):
            errors.append('Password must include at least one number.')
        if not re.search(r'[@#$%^&+=]',password1):
            errors.append('Password must include at least one special character.')
        
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_exists=User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists!")
        
        return email


    # Error validation for non-field errors
    def clean(self):
        cleaned_data=super().clean()
        password1=cleaned_data.get('password1')
        confirm_password=cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError('Password did not match!!')
        
        return cleaned_data

class CreateGroupForm(forms.ModelForm):
    permissions=forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    class Meta:
        model=Group
        fields=['name','permissions']

        widgets = {
            'name':forms.TextInput(
                attrs={
                    'placeholder':'Group Name',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            ),
            'permissions':forms.CheckboxSelectMultiple(
                attrs={
                    'class':'w-full p-4 my-2 border-2 rounded-md'
                }
            )
        }


class AssignRoleForm(forms.Form):
    role=forms.ModelChoiceField(queryset=Group.objects.all(),
                                empty_label='Select a role',
                                widget=forms.Select(
                                    attrs={
                                        'class':'w-full p-4 border-2 border-gray-200 rounded-md my-2'
                                    }
                                )
                                )
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','profile_image','phone_number']

        widgets={
            'username':forms.TextInput(
                attrs={
                    'placeholder':'Username',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            ),
            'first_name':forms.TextInput(
                attrs={
                    'placeholder':'first_name',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            ),
            'last_name':forms.TextInput(
                attrs={
                    'placeholder':'Last Name',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'placeholder':'demo@gmail.com',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md',
                }
            ),
            
            'phone_number':forms.TextInput(
                attrs={
                    'placeholder':'Phone Number',
                    'class':'w-full p-4 my-2 border-2 border-gray-400 rounded-md shadow-md'
                }
            )
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'class':'border w-full my-2 p-4 rounded-md',
                'placeholder':'username',
                "autofocus": True
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                "autocomplete": "current-password",
                'placeholder':'password',
                'class':'border w-full my-2 p-4 rounded-md'
            }
        )
    
    

class CustomPasswordChangeForm(PasswordChangeForm):
    pass

class CustomPasswordResetForm(PasswordResetForm):
    pass
    # def __init__(self, data = ..., files = ..., auto_id = ..., prefix = ..., initial = ..., error_class = ..., label_suffix = ..., empty_permitted = ..., field_order = ..., use_required_attribute = ..., renderer = ...):
    #     super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order, use_required_attribute, renderer)
    #     self.fields['email'].widget.attrs.update(
    #         {
    #             'placeholder':'Enter Your Email',
    #             'class':'w-full p-4 my-2 border-2 rounded-md border-gray-400'
    #         }
    #     )        

class CustomPasswordResetConfirmForm(SetPasswordForm):
    pass