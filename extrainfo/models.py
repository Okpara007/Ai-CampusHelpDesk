from django.db import models

from userschema.models import CustomUser


class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


STATUS = [
    ("New", "New"),
    ("Pending", "Pending"),
    ("Process", "Process"),
    ("closed", "Closed"),
]


class Appointment(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    services = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    dob = models.DateField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    appt_time = models.CharField(max_length=100, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, default="new")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.created_by.email


class Patient(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.full_name}"


class Doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    clinic = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Course(models.Model):
    name = models.CharField(max_length=150, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    duration = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    fees = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=80, default="General")
    published_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class StudentResource(models.Model):
    RESOURCE_TYPES = [
        ("timetable", "Timetable"),
        ("schedule", "Schedule"),
        ("booklet", "Booklet"),
        ("test_solution", "Test Solution"),
        ("video", "Video Link"),
        ("notice", "Notice"),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=30, choices=RESOURCE_TYPES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    file = models.FileField(upload_to="resources/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FAQEntry(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    keywords = models.CharField(
        max_length=255,
        help_text="Comma separated terms used for quick local matching.",
        blank=True,
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "FAQ entries"
        ordering = ["question"]

    def __str__(self):
        return self.question


class AssessmentRecord(models.Model):
    TYPE_WEEKLY = "weekly"
    TYPE_PT1 = "pt1"
    TYPE_PT2 = "pt2"

    ASSESSMENT_TYPES = [
        (TYPE_WEEKLY, "Weekly"),
        (TYPE_PT1, "PT1"),
        (TYPE_PT2, "PT2"),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assessment_records")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    subject = models.CharField(max_length=120)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=25)
    exam_date = models.DateField(null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_assessments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.email} - {self.get_assessment_type_display()} - {self.subject}"


class ContentAuditLog(models.Model):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"

    TYPE_ANNOUNCEMENT = "announcement"
    TYPE_RESOURCE = "resource"
    TYPE_FAQ = "faq"

    ACTION_CHOICES = [
        (ACTION_CREATE, "Create"),
        (ACTION_UPDATE, "Update"),
        (ACTION_DELETE, "Delete"),
    ]
    TYPE_CHOICES = [
        (TYPE_ANNOUNCEMENT, "Announcement"),
        (TYPE_RESOURCE, "Resource"),
        (TYPE_FAQ, "FAQ"),
    ]

    actor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    object_id = models.PositiveIntegerField()
    summary = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_action_display()} {self.get_content_type_display()} #{self.object_id}"
