from django.db import models

# Create your models here.
class BirthdayDiscount(models.Model):
    title = models.CharField(max_length=255)
    title_hash = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=255)
    expire_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    is_push = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "birthday_discounts"
        ordering = ['-created_at']

class DeliveryCoupon(models.Model):
    section_title = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    expire_date = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    code = models.CharField(max_length=255, null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    content_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "delivery_coupons"
        ordering = ['-created_at']
        def __str__(self):
            return f"{self.platform} - {self.section_title}"
        
class FreeGames4Gamers(models.Model):
    title = models.CharField(max_length=255)
    title_hash = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255)
    publish_date = models.DateField(null=True, blank=True)
    is_push = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "free_games_4gamers"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
class GovOJTs(models.Model):
    training_unit_url = models.CharField(max_length=255, unique=True)
    course_code = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    training_count = models.CharField(max_length=255, blank=True, null=True)
    training_hours = models.CharField(max_length=255, blank=True, null=True)
    student_cost = models.CharField(max_length=255, blank=True, null=True)
    government_cost = models.CharField(max_length=255, blank=True, null=True)
    training_location = models.CharField(max_length=255, blank=True, null=True)
    registration_start_at = models.CharField(max_length=255, blank=True, null=True)
    registration_end_at = models.CharField(max_length=255, blank=True, null=True)
    notified_3days_before = models.DateTimeField(null=True, blank=True)
    notified_1day_before = models.DateTimeField(null=True, blank=True)
    notified_1hour_before = models.DateTimeField(null=True, blank=True)
    enrollment_status = models.CharField(max_length=255, blank=True, null=True)
    scheduled_start_date = models.CharField(max_length=255, blank=True, null=True)
    scheduled_end_date = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "gov_ojts"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
class YoutubeVideos(models.Model):
    video_id = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    channel_name = models.CharField(max_length=255)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "youtube_videos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.channel_name})"
    
class Rent591(models.Model):
    title = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    price_info = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rent_591"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.region})"