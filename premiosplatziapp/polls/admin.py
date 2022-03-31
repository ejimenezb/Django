from django.contrib import admin
from .models import Choice, Question

#Modelo Choices en el administrador
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

#Modelo Question en el administrador
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)

# Documentacion del admin-django
# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/