from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# ---------------- Validators ----------------
def validate_image_file(value):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = value.name.split('.')[-1].lower()
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(allowed_extensions)}')

# ---------------- UserDetail Model ----------------
class UserDetail(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    COMPANY_RANK_CHOICES = [
        ('director', 'Director'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_detail')
    profile_image = models.ImageField(
        upload_to='userdetail/images/',
        blank=True,
        validators=[validate_image_file]
    )
    mobile_contact = models.CharField(max_length=15, unique=True)  # Not null
    email = models.EmailField(blank=True, null=True)  # Nullable
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False)  # Not null
    age = models.PositiveIntegerField(blank=False, null=False)  # Not null
    region = models.CharField(max_length=100)  # Not null
    company_rank = models.CharField(max_length=50, choices=COMPANY_RANK_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=100)  # Not null
    website_link = models.URLField(blank=True, null=True)
    facebook_account = models.CharField(max_length=100) 
    instagram_account = models.CharField(max_length=100) 
    twitter_account = models.CharField(max_length=100)
    youtube_account = models.URLField(blank=True, null=True) 

    def __str__(self):
        return f'{self.user.username} - Details'

# ---------------- PartnerForm Model ----------------
class PartnerForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partner")
    full_name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)  # Added max_length
    mobile_no = models.CharField(max_length=15)  # Required
    email = models.EmailField(blank=True, null=True)
    region = models.CharField(max_length=100)
    partner_rank = models.CharField(max_length=100)
    profile_image = models.ImageField(
        upload_to="Partners/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Partner: {self.full_name}"

# ---------------- ClientForm Model ----------------
class ClientForm(models.Model):
    CLIENT_COMPANY_CHOICES = [
        ('LMT', 'LIMITED'),
        ('INV', 'INVESTMENT'),
        ('COMP', 'COMPANY'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client")
    title = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)  # Required
    email = models.EmailField(blank=True, null=True)
    region = models.CharField(max_length=100)
    company_choice = models.CharField(max_length=100, choices=CLIENT_COMPANY_CHOICES)  # Fixed to use choices
    profile_image = models.ImageField(
        upload_to="Clients/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Client: {self.title}"

# ---------------- CertificateForm Model ----------------
class CertificateForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificate")
    certificate_name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="Certificates/images/",
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Certificate: {self.certificate_name}"
    
    
class Log(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    home_page_count = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Home: {self.home_page_count} - {self.user.username if self.user else 'Anonymous'}"
