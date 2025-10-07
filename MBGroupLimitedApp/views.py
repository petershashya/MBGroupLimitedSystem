from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.timezone import now
import pytz
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse

from .forms import (
    SuperUserRegistrationForm,
    PartnerModelForm,
    ClientModelForm,
    CertificateModelForm
)
from .models import (
     UserDetail, PartnerForm,
      ClientForm, CertificateForm, Log
)




def home(request):
    log, created = Log.objects.get_or_create(
            user_id=None
        )
    if not created:
            log.home_page_count += 1
    log.save()
        
    aboutdetails = UserDetail.objects.order_by("company_rank").first()
    userdetails= UserDetail.objects.order_by("company_rank").first()
    partners= PartnerForm.objects.all()
    clients= ClientForm.objects.all()
    certificates= CertificateForm.objects.all()
    context = {
        "userdetail": userdetails,
        "partners": partners,
        "certificates": certificates,
        "clients": clients,
        "aboutdetail":aboutdetails,
    }
    return render(request, "index.html",context)


def service(request):
    aboutdetails = UserDetail.objects.order_by("company_rank").first()
    userdetails= UserDetail.objects.order_by("company_rank").first()
    context = {
        "userdetail": userdetails,
        "aboutdetail":aboutdetails,
    }
    return render(request, "service.html", context)


@login_required
def account(request):
    aboutdetails = UserDetail.objects.order_by("company_rank").first()
    userdetails = UserDetail.objects.get(user=request.user)
    user = User.objects.get(username=request.user)
    # partner= PartnerForm.objects.get(user=request.user)
    partner= PartnerForm.objects.order_by("partner_rank").first()
    
    # : Fetch related models
    partners = PartnerForm.objects.all()
    clients = ClientForm.objects.all()
    certificates = CertificateForm.objects.all()

    now = timezone.now()
    one_week_ago = now - timezone.timedelta(weeks=1)

    # Active users (last login within a week)
    active_users = User.objects.filter(last_login__gte=one_week_ago, is_active=True)
    active_users_count = active_users.count()

    # Non-staff (normal) users
    non_staff_users = User.objects.filter(is_staff=False, is_superuser=False)
    non_staff_users_count = non_staff_users.count()

    # Staff (superusers)
    staff_users = User.objects.filter(is_staff=True, is_superuser=True)
    staff_users_count = staff_users.count()
    
    partner_count=partners.count()
    client_count=clients.count()
    certificate_count=certificates.count()
    

    # Homepage logs total
    homepage_logs = Log.objects.aggregate(total=Sum('home_page_count'))['total'] or 0

    if request.method == 'POST':
        if 'delete_selected' in request.POST:
            user_ids = request.POST.getlist('selected_users')
            User.objects.filter(id__in=user_ids).delete()
            return redirect('admin_dashboard')

    context = {
        "user": user,
        "userdetail": userdetails,
        "partners": partners,
        "partner":partner,
        "clients": clients,
        "certificates": certificates,
        "staff_users": staff_users,
        "active_users_count": active_users_count,
        "non_staff_users_count": non_staff_users_count,
        "staff_users_count": staff_users_count,
        "partner_count":partner_count,
        "client_count":client_count,
        "certificate_count":certificate_count,
        "homepage_logs": homepage_logs,
        "aboutdetail":aboutdetails,
    }
    return render(request, "account.html", context)


# ---------------- Partner View ----------------
@login_required
def post_partner(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['director', 'vice_director']:
        messages.error(request, "You do not have permission to register a partner.")
        return redirect('/')

    if request.method == 'POST':
        form = PartnerModelForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            mobile_no = form.cleaned_data['mobile_no']
            existing = PartnerForm.objects.filter(
                user=request.user,
                full_name__iexact=full_name,
                mobile_no=mobile_no
            ).exists()
            if existing:
                messages.warning(request, "You have already registered this partner.")
                return redirect('/')

            partner = form.save(commit=False)
            partner.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            partner.date_created = datetime.now(tz=user_tz)
            partner.date_modified = datetime.now(tz=user_tz)
            partner.save()
            messages.success(request, "Partner registered successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = PartnerModelForm()
        return render(request, 'partner_form.html', {'partner_form': form})


# ---------------- Client View ----------------
@login_required
def post_client(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['director', 'vice_director']:
        messages.error(request, "You do not have permission to register a client.")
        return redirect('/')

    if request.method == 'POST':
        form = ClientModelForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            mobile_no = form.cleaned_data['mobile_no']
            existing = ClientForm.objects.filter(
                user=request.user,
                title__iexact=title,
                mobile_no=mobile_no
            ).exists()
            if existing:
                messages.warning(request, "You have already registered this client.")
                return redirect('/')

            client = form.save(commit=False)
            client.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            client.date_created = datetime.now(tz=user_tz)
            client.date_modified = datetime.now(tz=user_tz)
            client.save()
            messages.success(request, "Client registered successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = ClientModelForm()
        return render(request, 'client_form.html', {'client_form': form})



# ---------------- Certificate View ----------------
@login_required
def post_certificate(request):
    user_rank = getattr(request.user.user_detail, 'company_rank', '').lower()
    if user_rank not in ['director', 'vice_director']:
        messages.error(request, "You do not have permission to register a certificate.")
        return redirect('/')

    if request.method == 'POST':
        form = CertificateModelForm(request.POST, request.FILES)
        if form.is_valid():
            certificate_name = form.cleaned_data['certificate_name']
            existing = CertificateForm.objects.filter(
                user=request.user,
                certificate_name__iexact=certificate_name
            ).exists()
            if existing:
                messages.warning(request, "You have already registered this certificate.")
                return redirect('/')

            certificate = form.save(commit=False)
            certificate.user = request.user
            user_tz = pytz.timezone('Africa/Dar_es_Salaam')
            certificate.date_created = datetime.now(tz=user_tz)
            certificate.date_modified = datetime.now(tz=user_tz)
            certificate.save()
            messages.success(request, "Certificate registered successfully.")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your submission.")
            return redirect('/')
    else:
        form = CertificateModelForm()
        return render(request, 'certificate_form.html', {'certificate_form': form})



# start edit and delete for partner, clients and certificates

# ---------- PARTNERS ----------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def partner_edit(request, partner_id):
    partner = get_object_or_404(PartnerForm, id=partner_id)  
    if request.method == "POST":
        form = PartnerModelForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, "Partner updated successfully.")
            return redirect("account")
    else:
        form = PartnerModelForm(instance=partner)

    # return modal HTML
    return render(request, "edit_partner.html", {
        "form": form,
        "partner_obj": partner  
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def partner_delete(request, partner_id):
    partner = get_object_or_404(PartnerForm, id=partner_id) 
    if request.method == "POST":
        partner.delete()
        messages.success(request, "Partner deleted successfully.")
        return redirect("account")

    # return modal HTML
    return render(request, "delete_partner.html", {
        "partner_obj": partner  
    })
    
# ---------- CLIENTS ----------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def client_edit(request, client_id):
    client = get_object_or_404(ClientForm, id=client_id)
    if request.method == "POST":
        form = ClientModelForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully.")
            return redirect("account")
    else:
        form = ClientModelForm(instance=client)
    return render(request, "edit_client.html", {"form": form, "client_obj": client})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def client_delete(request, client_id):
    client = get_object_or_404(ClientForm, id=client_id)
    if request.method == "POST":
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect("account")
    return render(request, "delete_client.html", {"client_obj": client})

# ---------- CERTIFICATES ----------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def certificate_edit(request, certificate_id):
    certificate = get_object_or_404(CertificateForm, id=certificate_id)
    if request.method == "POST":
        form = CertificateModelForm(request.POST, request.FILES, instance=certificate)
        if form.is_valid():
            form.save()
            messages.success(request, "Certificate updated successfully.")
            return redirect("account")
    else:
        form = CertificateModelForm(instance=certificate)
    return render(request, "edit_certificate.html", {"form": form, "certificate_obj": certificate})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def certificate_delete(request, certificate_id):
    certificate = get_object_or_404(CertificateForm, id=certificate_id)
    if request.method == "POST":
        certificate.delete()
        messages.success(request, "Certificate deleted successfully.")
        return redirect("account")
    return render(request, "delete_certificate.html", {"certificate_obj": certificate})




# ---------------- Register & Authentication ----------------
def register_admin(request):
    if request.method == 'POST':
        # SuperUser (Admin Registration)
        if 'register_admin' in request.POST:
            form = SuperUserRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                admin = form.save(commit=False)
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
                form.save(commit=True)
                messages.success(request, "Admin registered successfully.")
                return redirect('login_admin')
            else:
                return render(request, 'register_admin.html', {'admin_form': form})
    else:
        admin_form = SuperUserRegistrationForm()

    if request.resolver_match.url_name == 'register_admin':
        return render(request, 'register_admin.html', {'admin_form': admin_form})

def login_admin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        login_method = request.POST.get('login_method')
        login_input = request.POST.get('login_input')
        password = request.POST.get('password')
        user = None

        if login_method == 'username':
            user = authenticate(request, username=login_input, password=password)
        elif login_method == 'email':
            try:
                user_obj = User.objects.get(email=login_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        elif login_method == 'mobile':
            try:
                user_detail = UserDetail.objects.get(mobile_contact=login_input)
                user = authenticate(request, username=user_detail.user.username, password=password)
            except UserDetail.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('/')
        else:
            messages.error(request, "Invalid login credentials.")
    return render(request, 'login.html', {'form': form})

@login_required
def logout_admin(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login_admin')




#start edit and delete for staffs
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.save()
        messages.success(request, "User edited successfully.")
        return redirect(reverse('account'))  # go back to account page

    context = {'user_obj': user}
    return render(request, 'edit_user.html', context)

@login_required
@user_passes_test(is_superuser)
def admin_user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect(reverse('account'))  # go back to account page

    return render(request, 'delete_user.html', {'user_obj': user})
    
    
    
    
   #edit and delete admins
   
# def is_superuser(user):
#     return user.is_superuser

# @login_required
# @user_passes_test(is_superuser)
# def admin_superuser_edit(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     userdetail = get_object_or_404(UserDetail, id=user_id)

#     if request.method == 'POST':
#         form = SuperUserRegistrationForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Admin details updated successfully.")
#             return redirect(reverse('account'))  # go back to account page
#     else:
#         form = SuperUserRegistrationForm(instance=user)

#     context = {
#         'superuser_obj': user,
#         'superuserdetail':userdetail,
#         'admin_form': form
#     }
#     return render(request, 'edit_superuser.html', context)

# @login_required
# @user_passes_test(is_superuser)
# def admin_superuser_delete(request, user_id):
#     user = get_object_or_404(User, id=user_id)

#     if request.method == 'POST':
#         user.delete()
#         messages.success(request, "Admin deleted successfully.")
#         return redirect(reverse('account'))  # go back to account page

#     return render(request, 'delete_superuser.html', {'superuser_obj': user}) 


# --- Check function to restrict access to superusers ---
def is_superuser(user):
    return user.is_superuser

# --- Edit Super User ---
@login_required
@user_passes_test(is_superuser)
def admin_superuser_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = SuperUserRegistrationForm(request.POST or None, request.FILES or None, instance=user)

    # Load existing details into form initial values
    if request.method == 'GET':
        try:
            user_detail = UserDetail.objects.get(user=user)
            form.initial.update({
                'mobile_contact': user_detail.mobile_contact,
                'email': user_detail.email,
                'gender': user_detail.gender,
                'age': user_detail.age,
                'region': user_detail.region,
                'address': user_detail.address,
                'company_rank': user_detail.company_rank,
                'facebook_account': user_detail.facebook_account,
                'instagram_account': user_detail.instagram_account,
                'twitter_account': user_detail.twitter_account,
                'youtube_account': user_detail.youtube_account,
                'website_link': user_detail.website_link,
                'profile_image': user_detail.profile_image,
            })
        except UserDetail.DoesNotExist:
            pass

    # --- When form is submitted ---
    if request.method == 'POST':
        if 'save' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "Super user updated successfully.")
                return redirect(reverse('account'))  # go back to account page
            else:
                messages.error(request, "Please correct the errors below.")
        elif 'delete' in request.POST:
            form.delete_user()
            messages.success(request, "Super user deleted successfully.")
            return redirect(reverse('account'))

    return render(request, 'edit_user.html', {'admin_form': form, 'user_obj': user})

# --- Delete Super User (separate view if using confirmation page) ---
@login_required
@user_passes_test(is_superuser)
def admin_superuser_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = SuperUserRegistrationForm(instance=user)
        form.delete_user()
        messages.success(request, "User deleted successfully.")
        return redirect(reverse('account'))

    return render(request, 'delete_user.html', {'user_obj': user})
