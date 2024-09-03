from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import views as auth_views
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import CustomUser
from django.urls import reverse_lazy
from .decorators import redirect_if_authenticated
from recomendations.forms import UserGenreForm
from recomendations.models import UserGenre


@redirect_if_authenticated
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send verification email
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('authentication/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            return redirect('email_verification_sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})



@redirect_if_authenticated
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if 'remember_me' in request.POST:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser session
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def logouT(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/account_activation_success.html')
    else:
        return render(request, 'authentication/account_activation_invalid.html')




@login_required(login_url='/login')
def profile_view(request):
    user = request.user
    genre_form = UserGenreForm(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        # genre_form = UserGenreForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # UserGenre.objects.filter(user=user).delete()
            # for genre in genre_form.cleaned_data['genres']:
                # UserGenre.objects.create(user=user, name=genre.name)
            messages.success(request, 'Your profile and genres have been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'genre_form': genre_form,
    }

    return render(request, 'authentication/profile.html', context)


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'authentication/password_reset_complete.html'

def email_verification_sent(request):
    return render(request, 'authentication/email_verification_sent.html')

def resend_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                activation_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')

                # Send the activation email
                subject = 'Activate Your Account'
                message = render_to_string('authentication/email_verification.html', {
                    'user': user,
                    'domain': request.get_host(),
                    'uid': uid,
                    'token': token,
                })
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
                
                return render(request, 'authentication/resend_activation_success.html')
        except User.DoesNotExist:
            # Optionally, you could handle the case where the email does not exist
            pass

    return render(request, 'authentication/resend_activation_request.html')