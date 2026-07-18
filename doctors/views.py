from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.core.files.storage import default_storage
from datetime import datetime

from .models import Blogs, Comments, Category
from users.models import Doctors, Specialty
from users.forms import ProfileForm, PasswordChangeForm
from .forms import BlogForm, CommentForm
from core.services import BlogService, DoctorService, PaginationService, UserService
from core.constants import TemplateName, ContextKey, MessageLevel, Pagination

User = get_user_model()


@login_required(login_url='/login')
def doctor_dashboard(request):
    doctor = request.user.doctors
    stats = DoctorService.get_doctor_stats(doctor)
    return render(request, TemplateName.DOCTOR_DASHBOARD, stats)


@login_required(login_url='/login')
def doctor_profile(request):
    specialities = Specialty.objects.all()
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm()
    updated_profile = False
    updated_password = False

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                user = profile_form.save(commit=False)
                if request.user.id_address:
                    addr = request.user.id_address
                    addr.address_line = profile_form.cleaned_data.get('address_line', addr.address_line)
                    addr.region = profile_form.cleaned_data.get('region', addr.region)
                    addr.city = profile_form.cleaned_data.get('city', addr.city)
                    addr.code_postal = profile_form.cleaned_data.get('code_postal', addr.code_postal)
                    addr.save()
                specialty_name = request.POST.get('Speciality')
                if specialty_name:
                    doctor_profile = request.user.doctors
                    doctor_profile.specialty = Specialty.objects.get(name=specialty_name)
                    doctor_profile.bio = request.POST.get('bio', '')
                    doctor_profile.save()
                user.save()
                updated_profile = True
                messages.success(request, 'Profile updated successfully.', extra_tags=MessageLevel.SUCCESS)
            else:
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

        elif 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                if not request.user.check_password(password_form.cleaned_data['current_password']):
                    messages.error(request, 'Current password is incorrect.')
                else:
                    request.user.set_password(password_form.cleaned_data['new_password'])
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    updated_password = True
                    messages.success(request, 'Password updated successfully.', extra_tags=MessageLevel.SUCCESS)
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

    return render(request, TemplateName.DOCTOR_PROFILE, {
        'basicdata': request.user,
        'updated_profile_successfully': updated_profile,
        'updated_password_successfully': updated_password,
        'specialities': specialities,
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required(login_url='/login')
def doctor_blogs(request):
    base_template = UserService.get_base_template(request.user)
    blogs = BlogService.get_published_blogs()
    categories = Category.objects.all()
    _, blogs_page = PaginationService.paginate(blogs, request.GET.get('page'))

    return render(request, TemplateName.DOCTOR_BLOGS, {
        'blogs': blogs_page,
        ContextKey.CATEGORIES: categories,
        ContextKey.BASE_TEMPLATE: base_template,
    })


@login_required(login_url='/login')
def search_blogs(request):
    base_template = UserService.get_base_template(request.user)
    keyword = request.GET.get('keyword', '')
    blogs = BlogService.search_blogs(keyword) if keyword else BlogService.get_published_blogs()
    categories = Category.objects.all()
    _, blogs_page = PaginationService.paginate(blogs, request.GET.get('page'))

    return render(request, TemplateName.DOCTOR_BLOGS, {
        'blogs': blogs_page,
        ContextKey.CATEGORIES: categories,
        'searching': 1,
        'keyword': keyword,
        ContextKey.BASE_TEMPLATE: base_template,
    })


def blogs_category(request, cat):
    base_template = UserService.get_base_template(request.user) if request.user.is_authenticated else 'patients/base.html'
    category = get_object_or_404(Category, name=cat)
    blogs = BlogService.get_blogs_by_category(category)
    categories = Category.objects.all()
    _, blogs_page = PaginationService.paginate(blogs, request.GET.get('page'))

    return render(request, TemplateName.DOCTOR_BLOGS, {
        'blogs': blogs_page,
        ContextKey.CATEGORIES: categories,
        ContextKey.BASE_TEMPLATE: base_template,
    })


@login_required(login_url='/login')
def upload_blog(request, blog_id=None):
    blog = get_object_or_404(Blogs, pk=blog_id) if blog_id else Blogs()
    form = BlogForm(instance=blog if blog_id else None)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog if blog_id else None)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.doctor = get_object_or_404(Doctors, user=request.user)
            blog.posted_at = datetime.now()
            blog.save()
            msg = 'Blog published successfully!' if blog.is_published else 'Blog saved as draft.'
            messages.success(request, msg, extra_tags=MessageLevel.SUCCESS)
            return redirect('upload_blog')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, TemplateName.UPLOAD_BLOG, {
        'user_name': request.user.username,
        'total_categories': Category.objects.all(),
        'blog': blog,
        'form': form,
    })


@login_required(login_url='/login')
def view_blog(request, blog_id):
    base_template = UserService.get_base_template(request.user)
    blog = get_object_or_404(Blogs.objects.select_related('doctor__user', 'id_category'), blog_id=blog_id)
    related_blogs = BlogService.get_related_blogs(blog, blog_id)
    recent_blogs = BlogService.get_recent_blogs(blog_id)
    categories = Category.objects.all()
    comments = Comments.objects.filter(blog=blog).select_related('user')

    return render(request, TemplateName.VIEW_BLOG, {
        'related_blogs': related_blogs,
        'recent_blogs': recent_blogs,
        'blog': blog,
        ContextKey.CATEGORIES: categories,
        'comments': comments,
        ContextKey.BASE_TEMPLATE: base_template,
        'comment_form': CommentForm(),
    })


@login_required(login_url='/login')
def post_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            blog_id = request.POST.get('id')
            blog = get_object_or_404(Blogs, blog_id=blog_id)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.commented_at = datetime.now()
            comment.save()
            messages.success(request, 'Comment posted.', extra_tags=MessageLevel.SUCCESS)
            return redirect(reverse('blog', args=[int(blog_id)]))
    return redirect('doctor_blogs')


@login_required(login_url='/login')
def doctor_myblogs(request):
    author = get_object_or_404(Doctors, user=request.user)
    blogs = BlogService.get_doctor_blogs(author).filter(is_published=True)
    categories = Category.objects.all()
    _, blogs_page = PaginationService.paginate(blogs, request.GET.get('page'))

    return render(request, TemplateName.DOCTOR_BLOGS, {
        'blogs': blogs_page,
        ContextKey.CATEGORIES: categories,
        ContextKey.BASE_TEMPLATE: 'doctors/base.html',
    })


@login_required(login_url='/login')
def doctor_drafts(request):
    author = get_object_or_404(Doctors, user=request.user)
    drafts = BlogService.get_doctor_blogs(author).filter(is_published=False)
    categories = Category.objects.all()
    _, drafts_page = PaginationService.paginate(drafts, request.GET.get('page'))

    return render(request, TemplateName.DOCTOR_DRAFTS, {
        'drafts': drafts_page,
        ContextKey.CATEGORIES: categories,
    })


@login_required(login_url='/login')
def view_appointments(request):
    if request.method == 'POST':
        status = request.POST.get("status")
        app_id = request.POST.get("app")
        from core.services import AppointmentService
        try:
            AppointmentService.update_appointment_status(app_id, status)
            messages.success(request, f'Appointment status updated to {status}.', extra_tags=MessageLevel.SUCCESS)
        except Exception as e:
            messages.error(request, f'Failed to update appointment: {str(e)}')

    doctor = request.user.doctors
    appointments = AppointmentService.get_doctor_appointments(doctor)

    return render(request, TemplateName.VIEW_APPOINTMENTS, {
        ContextKey.APPOINTMENTS: appointments,
        'filter_status': request.GET.get('filter_status'),
        'filter_date': request.GET.get('filter_date'),
        'filter_patient_name': request.GET.get('filter_patient_name'),
    })
