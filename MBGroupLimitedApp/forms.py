from django import forms
from django.contrib.auth.models import User
from .models import UserDetail, PartnerForm, ClientForm, CertificateForm

# Choice constants (must match the models)
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

COMPANY_RANK_CHOICES = [
    ('director', 'Director'),
]

CLIENT_COMPANY_CHOICES = [
        ('LMT', 'LIMITED'),
        ('INV', 'INVESTMENT'),
        ('COMP', 'COMPANY'),
]

# ---------------- SuperUser Registration Form ----------------
class SuperUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    mobile_contact = forms.CharField(max_length=15, required=True, label='Mobile Number')
    email = forms.EmailField(required=False, label='Email Address')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    age = forms.IntegerField(required=True, min_value=1)
    region = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True, label="Address")
    company_rank = forms.ChoiceField(choices=COMPANY_RANK_CHOICES, required=False)
    facebook_account = forms.CharField(max_length=100, required=True)
    instagram_account = forms.CharField(max_length=100, required=True)
    twitter_account = forms.CharField(max_length=100, required=True)
    youtube_account = forms.URLField(required=True)
    website_link = forms.CharField(required=True)
    profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def clean_mobile_contact(self):
        mobile_contact = self.cleaned_data.get('mobile_contact')
        if UserDetail.objects.filter(mobile_contact=mobile_contact).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile_contact
    
    def clean_company_rank(self):
        company_rank = self.cleaned_data.get('company_rank')
        if UserDetail.objects.filter(company_rank=company_rank).exists():
            raise forms.ValidationError("A Company Rank already registered.")
        return company_rank

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            UserDetail.objects.create(
                user=user,
                profile_image=self.cleaned_data.get('profile_image'),
                mobile_contact=self.cleaned_data['mobile_contact'],
                email=self.cleaned_data.get('email'),
                gender=self.cleaned_data.get('gender'),
                age=self.cleaned_data.get('age'),
                region=self.cleaned_data['region'],
                address=self.cleaned_data.get('address'),
                company_rank=self.cleaned_data.get('company_rank'),
                facebook_account = self.cleaned_data.get('facebook_account'),
                instagram_account = self.cleaned_data.get('instagram_account'),
                twitter_account = self.cleaned_data.get('twitter_account'),
                youtube_account = self.cleaned_data.get('youtube_account'),
                website_link = self.cleaned_data.get('website_link'),
            )
        return user
    
# # forms.py
# class SuperUserEditForm(forms.ModelForm):
#     mobile_contact = forms.CharField(max_length=15, required=True, label='Mobile Number')
#     email = forms.EmailField(required=False, label='Email Address')
#     gender = forms.ChoiceField(choices=UserDetail.GENDER_CHOICES, required=True)
#     age = forms.IntegerField(required=True, min_value=1)
#     region = forms.CharField(max_length=100, required=True)
#     address = forms.CharField(max_length=100, required=True, label="Address")
#     company_rank = forms.ChoiceField(choices=UserDetail.COMPANY_RANK_CHOICES, required=False)
#     facebook_account = forms.CharField(max_length=100, required=True)
#     instagram_account = forms.CharField(max_length=100, required=True)
#     twitter_account = forms.CharField(max_length=100, required=True)
#     youtube_account = forms.URLField(required=True)
#     website_link = forms.CharField(required=True)
#     profile_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name']
   
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop("user_instance", None)
#         super().__init__(*args, **kwargs)
#         if user and hasattr(user, "user_detail"):
#             detail = user.user_detail
#             self.fields['mobile_contact'].initial = detail.mobile_contact
#             self.fields['email'].initial = detail.email
#             self.fields['gender'].initial = detail.gender
#             self.fields['age'].initial = detail.age
#             self.fields['region'].initial = detail.region
#             self.fields['address'].initial = detail.address
#             self.fields['company_rank'].initial = detail.company_rank
#             self.fields['facebook_account'].initial = detail.facebook_account
#             self.fields['instagram_account'].initial = detail.instagram_account
#             self.fields['twitter_account'].initial = detail.twitter_account
#             self.fields['youtube_account'].initial = detail.youtube_account
#             self.fields['website_link'].initial = detail.website_link
#             self.fields['profile_image'].initial = detail.profile_image

#     def save(self, commit=True, user_instance=None):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#             detail, created = UserDetail.objects.get_or_create(user=user)
#             detail.mobile_contact = self.cleaned_data['mobile_contact']
#             detail.email = self.cleaned_data['email']
#             detail.gender = self.cleaned_data['gender']
#             detail.age = self.cleaned_data['age']
#             detail.region = self.cleaned_data['region']
#             detail.address = self.cleaned_data['address']
#             detail.company_rank = self.cleaned_data['company_rank']
#             detail.facebook_account = self.cleaned_data['facebook_account']
#             detail.instagram_account = self.cleaned_data['instagram_account']
#             detail.twitter_account = self.cleaned_data['twitter_account']
#             detail.youtube_account = self.cleaned_data['youtube_account']
#             detail.website_link = self.cleaned_data['website_link']
#             if self.cleaned_data.get('profile_image'):
#                 detail.profile_image = self.cleaned_data['profile_image']
#             detail.save()
#         return user
    
# ---------------- Partner Form ----------------
class PartnerModelForm(forms.ModelForm):
    class Meta:
        model = PartnerForm
        fields = [
            'full_name',
            'description',
            'mobile_no',
            'email',
            'region',
            'partner_rank',
            'profile_image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
        }
        labels = {
            'full_name': 'Full Name',
            'description': 'Description',
            'mobile_no': 'Mobile Number',
            'email': 'Email',
            'region': 'Region',
            'partner_rank': 'Partner Rank',
            'profile_image': 'Profile Image',
        }

# ---------------- Client Form ----------------
class ClientModelForm(forms.ModelForm):
    class Meta:
        model = ClientForm
        fields = [
            'title',
            'mobile_no',
            'email',
            'region',
            'company_choice',
            'profile_image',
        ]
        # widgets = {
        #     'company_choice':  forms.ChoiceField(choices=CLIENT_COMPANY_CHOICES, required=True)
        # }
        labels = {
            'title': 'Client Title',
            'mobile_no': 'Mobile Number',
            'email': 'Email',
            'region': 'Region',
            'company_choice': 'Company Type',
            'profile_image': 'Profile Image',
        }

# ---------------- Certificate Form ----------------
class CertificateModelForm(forms.ModelForm):
    class Meta:
        model = CertificateForm
        fields = [
            'certificate_name',
            'image',
        ]
        labels = {
            'certificate_name': 'Certificate Name',
            'image': 'Certificate Image',
        }