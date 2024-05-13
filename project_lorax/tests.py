from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, Client, override_settings
from .models import ReportedIssue
from django.contrib.auth.models import User, Permission
from django.urls import reverse


class ProjectTest(TestCase):
    def setUp(self):
        self.client = Client()

        ReportedIssue.objects.all().delete()
        issues_data = [
            {
                'id': 1,
                'author_username': 'user1',
                'report_text': 'Excessive waste issue',
                'organization_name': 'Org A',
                'report_name': 'Waste Report',
                'status': 'New',
                'report_type': ReportedIssue.ReportType.WASTE
            },
            {
                'id': 2,
                'author_username': 'user2',
                'report_text': 'Pollution concern',
                'organization_name': 'Org B',
                'report_name': 'Pollution Report',
                'status': 'In Progress',
                'report_type': ReportedIssue.ReportType.POLLUTION
            },
            {
                'id': 3,
                'author_username': 'user3',
                'report_text': 'Nature destruction observed',
                'organization_name': 'Org C',
                'report_name': 'Nature Report',
                'status': 'Resolves',
                'report_type': ReportedIssue.ReportType.NATURE
            }
        ]

        for issue_data in issues_data:
            issue = ReportedIssue.objects.create(**issue_data)
            issue.save()

        user_type = ContentType.objects.get(app_label="auth", model="user")
        self.test_user = User.objects.create_user(
            username='testuser', password='password123')

        can_view_site_permission = Permission.objects.create(
            codename="view_site", name="can view site", content_type=user_type)
        self.test_user.user_permissions.add(can_view_site_permission)
        self.client.login(username="testuser", login="password123")

    def test_landing_view(self):
        resp = self.client.get("")
        self.assertTrue("landing.html" in [t.name for t in resp.templates])

    @override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.InMemoryStorage')
    def test_upload_file_wrong_method(self):
        resp = self.client.get("/upload/")
        self.assertTrue("upload.html" in [t.name for t in resp.templates])

    @override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.InMemoryStorage')
    def test_upload_file(self):
        resp = self.client.post("/upload/", {"title": "Test report here", "organization": "Chess Club",
                                "report_type": "P", "text": "This five year old beat me I'm suing"})

        model = (ReportedIssue.objects.filter(report_name="Test report here"))
        self.assertTrue(len(model) == 1)

    def test_search_by_organization(self):
        # Test searching by organization name
        response = self.client.get(reverse('search'), {'query': 'Org B'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Waste Report')
        self.assertNotContains(response, 'Nature Report')

    def test_search_by_status(self):
        # Test searching by status

        response = self.client.get(reverse('search'), {
                              'status_filter': "New", })

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Pollution Report')
        self.assertNotContains(response, 'Nature Report')

    def test_search_by_report_type(self):
        # Test searching by report type
        response = self.client.get(reverse('search'), {
                              'report_type_filter': ReportedIssue.ReportType.POLLUTION})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Waste Report')
        self.assertNotContains(response, 'Nature Report')

    def test_search_no_results(self):
        # Test searching with no matching results
        response = self.client.get(reverse('search'), {'query': 'Nonexistent Org'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Waste Report')
        self.assertNotContains(response, 'Pollution Report')
        self.assertNotContains(response, 'Nature Report')


    #tests for model creation
    def test_check_reports_file_name(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        self.assertEquals("hello", post.file_name)

    def test_check_reports_author_username(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        self.assertEquals("joe", post.author_username)

    def test_check_reports_file_url(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        self.assertEquals("url", post.file_url)

    def test_check_reports_report_text(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        self.assertEquals("text", post.report_text)

    def test_check_reports_report_name(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        self.assertEquals("title", post.report_name)

    def test_check_reports_organization_name(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        self.assertEquals("organization", post.organization_name)

    def test_check_reports_report_type(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        self.assertEquals("report_type", post.report_type)

    def test_check_reports_new_text(self):
        post = ReportedIssue(
            file_name="hello", author_username="joe", file_url="url",
            report_text="text", report_name="title", organization_name="organization", report_type="report_type")
        post.report_text = "new text"
        self.assertEquals("new text", post.report_text)


