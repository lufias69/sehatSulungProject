# from django.db import models

# question_app/models.py

from django.db import models
from cloudinary.models import CloudinaryField  # Import CloudinaryField
from django.contrib.auth.models import User  # Import model User
from hash_app.utils import compute_model_hash, generate_unique_hash
from fitur_app.models import Feature


class QuestionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)  # Tambahkan field image
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class QuestionCategory(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)  # Menambahkan field umur (age)

    description = models.TextField(null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)  # Tambahkan field image
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from cloudinary.models import CloudinaryField

class Question(models.Model):
    # New field for priority
    priority = models.IntegerField(default=10)
    feature = models.ForeignKey('fitur_app.Feature', on_delete=models.CASCADE, related_name='questions', default=1)
    question_text = models.TextField()
    question_type = models.ForeignKey('QuestionType', related_name='questions', on_delete=models.CASCADE)
    category = models.ForeignKey('QuestionCategory', related_name='questions', on_delete=models.CASCADE)
    is_mandatory = models.BooleanField(default=True)

    image = CloudinaryField(resource_type='auto', null=True, blank=True)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)


    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    content_hash = models.CharField(max_length=64, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a new unique hash (using timestamp)
        self.content_hash = generate_unique_hash()  # Use the unique hash generator

        super().save(*args, **kwargs)

    def __str__(self):
        return self.choice_text


# from django.db import models
# from question_app.models import Question, Choice
#
# class UserAnswer(models.Model):
#     user_name = models.CharField(max_length=255)
#     question = models.ForeignKey(Question, related_name='user_answers', on_delete=models.CASCADE)
#     answer_text = models.TextField(null=True, blank=True)  # Digunakan untuk jawaban jenis essai
#     selected_choices = models.ManyToManyField(Choice, related_name='user_choice_answers', blank=True)  # Untuk pilihan ganda/centang
#     submitted_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Answer by {self.user_name} on {self.submitted_at}"


# checkup/models.py

# from django.db import models

# from question_app.models import Question, Choice

# checkup/models.py

from django.db import models
from django.contrib.auth.models import User  # Import model User
# from question_app.models import Question, Choice  # Import model Question dan Choice

class UserAnswer(models.Model):
    user = models.ForeignKey(User, related_name='user_answers', on_delete=models.CASCADE)  # Menghubungkan dengan model User
    question = models.ForeignKey(Question, related_name='user_answers', on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)  # Untuk pertanyaan essai
    selected_choices = models.ManyToManyField(Choice, related_name='user_choice_answers', blank=True)  # Untuk pilihan ganda/centang
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} on {self.submitted_at}"

