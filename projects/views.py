from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Me, Project
from . import forms


def home_page(request):
    me = Me.objects.get()
    proj = Project.objects.all()[0]
    pro = Project.objects.all()[1:3]
    return render(request, 'project/homepage.html', dict(pro=pro, proj=proj, me=me, section="home_page"))


def about_me(request):
    me = Me.objects.get()
    return render(request, "project/aboutpage.html", dict(me=me, section="about_me"))


def project(request):
    projects = Project.objects.all()
    paginator = Paginator(projects, 3)
    page = request.GET.get("page")

    try:
        project = paginator.page(page)
    except PageNotAnInteger:
        # if the page is not an integer deliver first page
        project = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver the last page of the results.
        project = paginator.page(paginator.num_pages)

    return render(request, 'project/projectpage.html',
                  dict(projects=projects, project=project, page=page))


def contact(request):
    try:
        submitted = False
        if request.method == "POST":
            email = request.POST.get("email_address")
            name = request.POST.get("name")
            subject = request.POST.get("subject")
            message = request.POST.get("message")
            message = name + " said, " + message

            if not email.endswith("com"):
                error = "Email should end with '.com,' please."
                return render(request, 'project/homepage.html', {'error': error, 'name': name})

            send_mail(subject=subject, message=message,
                      from_email=email,
                      recipient_list=['olaisaiah54@gmail.com'], fail_silently=False)

            return redirect('/contact?submitted=True')

        else:
            if "submitted" in request.GET:
                submitted = True
            return render(request, 'project/homepage.html', {'submitted': submitted})

    except ValueError:
        return render(request, 'project/homepage.html', {'error': "Bad request"})


def user_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect("projects:account")
                else:
                    return render(request, 'project/login.html', {'error': "Mayokun your account is not active"})
            else:
                return render(request, 'project/login.html', {'error': "Opps! It's only Isaiah Olaoye that can login😃😃"})

        return render(request, 'project/login.html', {})

    except ValueError:
        return render(request, 'project/login.html', {'error': "Bad request"})


@login_required
def dashboard(request):
    return render(request, 'project/account.html')


@login_required
def upload(request):
    try:
        if request.method == 'POST':
            form = forms.ProjectForm(request.POST)

            if form.is_valid():
                form = form.save(commit=False)

                if 'project_image' in request.FILES:
                    form.project_image = request.FILES.get("project_image")

                form.save()
                return redirect("projects:account")
            else:
                return render(request, 'project/upload.html', dict(form=form, error='Fill in the correct info.'))
        else:
            form = forms.ProjectForm()

        return render(request, 'project/upload.html', dict(form=form))

    except ValueError:
        return render(request, 'project/login.html', {'error': "Bad request"})


@login_required
def update(request):

    try:
        info = get_object_or_404(Me, id=1, user=request.user)
        if request.method == 'POST':
            update_form = forms.UserUpdateForm(instance=info,
                                               data=request.POST,
                                               files=request.FILES)
            if update_form.is_valid():
                update_form.save()
                return redirect("projects:account")

        else:
            update_form = forms.UserUpdateForm(instance=info)

        return render(request, 'project/updatepage.html', dict(form=update_form, info=info))

    except ValueError:
        return render(request, 'project/login.html', {'error': "Bad request"})


@login_required
def user_logout(request):
    logout(request)
    return redirect("projects:home_page")
