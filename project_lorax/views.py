from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404
from botocore.exceptions import NoCredentialsError
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from .models import ReportedIssue
from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from time import sleep
import json


def landing_view(request):
    user = request.user
    return render(request, 'landing.html', {"user": user})


def upload_file(request):
    # TODO: Create a post model for the file and user, and save that

    if request.method == 'POST':
        file = request.FILES.get('fileUpload', False)
        url = None
        file_name = None

        if file:
            default_storage.save(file.name, file)
            url = default_storage.url(file.name)
            file_name = file.name
        text = str(request.POST.get("text"))
        title = str(request.POST.get("title"))
        organization = str(request.POST.get("organization"))
        report_type = str(request.POST.get("report_type"))
        post = ReportedIssue(
            file_name=file_name, author_username=request.user.username, file_url=url,
            report_text=text, report_name=title, organization_name=organization, report_type=report_type)
        post.save()

        # TODO: If user is logged in, redirect to user profile, else redirect to landing page
        return render(request, 'landing.html')
    else:
        return render(request, 'upload.html')


def view_file(request, file_key):
    try:
        return redirect(file_key)

    except NoCredentialsError:
        raise ValueError


@login_required
def profile(request):
    if request.user.has_perm("sites.view_site"):
        return redirect(admin_profile)

    files = []
    for post in ReportedIssue.objects.filter(
            author_username=request.user.username):
        files.append({"name": post.report_name,
                      "id": post.id,
                      "organization": post.organization_name,
                      "status": post.status})

    output = {"files": files,
              "search": False}
    return render(request, "profile.html", output)


@permission_required("sites.view_site")
def admin_profile(request):
    files = []

    for post in ReportedIssue.objects.all():
        files.append({"name": post.report_name, "id": post.id,
                      "organization": post.organization_name, "status": post.status})
        output = {"files": files, }

    return render(request, 'profile.html', output)


def update_status(request):
    if request.method == "POST":
        id = request.POST.get("issue_id")
        issue = ReportedIssue.objects.get(pk=id)

        submitted_status = str(request.POST.get("status"))
        if submitted_status is not None and submitted_status != "None":
            issue.status = submitted_status
        issue.admin_comment = str(request.POST.get("comment"))
        issue.save()
    else:
        raise ValueError("womp womp")
    return view_reported_issue(request, id)


def delete_report(request):
    id = request.POST.get("issue_id")
    issue = ReportedIssue.objects.get(pk=id)
    issue.delete()
    return redirect(profile)


def view_reported_issue(request, reported_issue_id):
    reported_issue = get_object_or_404(ReportedIssue, pk=reported_issue_id)
    # is admin
    if request.user.has_perm('sites.view_site'):
        if reported_issue.status == "New":
            reported_issue.status = "In Progress"
            reported_issue.save()
        return render(request, "admin_reported_issue.html", {"reported_issue": reported_issue})
    return render(request, "user_reported_issue.html", {"reported_issue": reported_issue})


def search(request):

    organization = request.GET.get("query", "NONE")
    status = request.GET.get("status_filter", "NONE")
    report_type = request.GET.get("report_type_filter", "NONE")

    print(status)

    matches = ReportedIssue.objects.all()

    if not request.user.has_perm("sites.view_site"):
        matches = matches.filter(author_username=request.user.username)

    if organization != "NONE":
        matches = matches.filter(
            organization_name__icontains=organization)

    if status != "NONE":
        matches = matches.filter(status=status)

    if report_type != "NONE":
        matches = matches.filter(report_type=report_type)

    print(matches.values())
    print(status)
    posts = []
    for post in matches:
        posts.append({"name": post.report_name,
                      "id": post.id,
                      "organization": post.organization_name,
                      "status": post.status})

    output = {"files": posts,
              "search": True}
    return render(request, 'profile.html', output)


# used so logout redirects to a custom logout page, rather than staying on landing page
def logout(request):
    auth_logout(request)
    return render(request, "account/logout.html")

# def view_reported_issue(request, reported_issue_id):
#     return HttpResponse("You're looking at reported issue %s." % reported_issue_id)
#
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
