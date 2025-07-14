import json

from django.shortcuts import render
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from analisis_ai.models import HealthPredictionResult
from fitur_app.models import Feature
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def get_questions_by_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)

    # Ambil semua pertanyaan dengan choices-nya (prefetch choices untuk efisiensi)
    questions = feature.questions.prefetch_related('choices', 'question_type', 'category').all()

    # Format data dalam bentuk JSON
    questions_data = []

    for question in questions:
        question_data = {
            'id': question.id,
            'priority': question.priority,  # Menambahkan field priority
            'question_text': question.question_text,
            'question_type': {
                'id': question.question_type.id,
                'name': question.question_type.name  # Assuming 'name' exists in QuestionType
            },
            'category': {
                'id': question.category.id,
                'name': question.category.name  # Assuming 'name' exists in QuestionCategory
            },
            'is_mandatory': question.is_mandatory,
            'image': question.image.url if question.image else None,  # Menambahkan URL image
            'choices': {choice.id: choice.choice_text for choice in question.choices.all()}  # Choices dalam format key-value
        }
        questions_data.append(question_data)

    # Mengembalikan data dalam format JSON
    return JsonResponse({
        'feature': {
            'id': feature.id,
            'name': feature.name,
            'description': feature.description
        },
        'questions': questions_data,
        'questions_count': len(questions_data)
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feature, Session, UserResponse, Question





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feature, Session, UserResponse, Question, CheckupGroup


@login_required
def answer_questions(request, pk, checkup_group_id):
    feature = get_object_or_404(Feature, pk=pk)

    # Mendapatkan CheckupGroup berdasarkan ID yang diberikan
    checkup_group = get_object_or_404(CheckupGroup, id=checkup_group_id, user=request.user, is_deleted=False)

    # Membuat session baru untuk user dan fitur dengan checkup_group yang dipilih
    session = Session.objects.create(
        checkup_group=checkup_group,
        feature=feature
    )

    questions = feature.questions.prefetch_related('choices').all()

    if request.method == 'POST':
        # Menyimpan jawaban untuk setiap pertanyaan
        for question in questions:
            answer = request.POST.get(f'answer_{question.id}')

            if answer:  # Menyimpan jawaban Esai
                user_response = UserResponse.objects.create(
                    session=session,
                    question=question,
                    answer_text=answer if question.question_type.name == 'Essai' else None
                )

            # Menyimpan jawaban Multiple Choice
            if question.question_type.name == 'Multiple Choice':
                selected_choices = request.POST.getlist(f'answer_{question.id}')
                if selected_choices:
                    user_response.multiple_choice_answers.set(selected_choices)

        # Redirect ke feedback dengan checkup_group_id yang dipassing
        prediction_url = reverse('analisis_ai:make_health_prediction', args=[session.id])

        # Redirect ke URL yang telah dibuat
        return redirect(prediction_url)
        # return redirect('session_app:feedback', checkup_group_id=checkup_group.id, session_id=session.id)  # Pastikan checkup_group_id ada

    return render(request, 'session_app/answer_questions.html', {
        'feature': feature,
        'questions': questions,
        'checkup_group': checkup_group,  # Menyertakan CheckupGroup yang digunakan
    })
# def answer_questions(request, pk, checkup_group_id):
#     feature = get_object_or_404(Feature, pk=pk)
#
#     # Mendapatkan CheckupGroup berdasarkan ID yang diberikan
#     checkup_group = get_object_or_404(CheckupGroup, id=checkup_group_id, user=request.user, is_deleted=False)
#
#     # Membuat session baru untuk user dan fitur dengan checkup_group yang dipilih
#     session, created = Session.objects.get_or_create(
#         checkup_group=checkup_group,
#         feature=feature
#     )
#
#     questions = feature.questions.prefetch_related('choices').all()
#
#     if request.method == 'POST':
#         # Menyimpan jawaban untuk setiap pertanyaan
#         for question in questions:
#             answer = request.POST.get(f'answer_{question.id}')
#             if answer:
#                 user_response = UserResponse.objects.create(
#                     session=session,
#                     question=question,
#                     answer_text=answer if question.question_type.name == 'Essai' else None
#                 )
#                 if question.question_type.name == 'Multiple Choice':
#                     selected_choices = request.POST.getlist(f'choices_{question.id}')
#                     user_response.multiple_choice_answers.set(selected_choices)
#
#         return redirect('session_app:feedback')  # Redirect setelah menyimpan
#
#     return render(request, 'session_app/answer_questions.html', {
#         'feature': feature,
#         'questions': questions,
#         'checkup_group': checkup_group,  # Menyertakan CheckupGroup yang digunakan
#     })

# views.py

from django.shortcuts import render
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Session, UserResponse, Feature, CheckupGroup

def feedback_view(request, checkup_group_id, session_id):
    # Ambil CheckupGroup berdasarkan ID dan pastikan pengguna adalah pemiliknya
    checkup_group = get_object_or_404(CheckupGroup, id=checkup_group_id, user=request.user, is_deleted=False)

    # Ambil session berdasarkan session_id dan checkup_group
    session = get_object_or_404(Session, id=session_id, checkup_group=checkup_group)

    # Ambil UserResponses yang terkait dengan session ini
    user_responses = UserResponse.objects.filter(session=session)

    # Ambil fitur yang terkait dengan session ini
    feature = session.feature
    criteria_details = []
    health_recommendation = ""
    if HealthPredictionResult.objects.filter(session=session):
        x = HealthPredictionResult.objects.filter(session=session)
        for i in x:
            for j in i.criteria_details:
                print(j)
                criteria_details.append(j)
            health_recommendation = i.health_recommendation
            # print(i.criteria_details)
    else:
        x=[]
        print("no")

    return render(request, 'session_app/feedback.html', {
        'checkup_group': checkup_group,
        'user_responses': user_responses,
        'feature': feature,
        'criteria_details': criteria_details,
        'health_recommendation': health_recommendation,
        'HealthPredictionResult':x
    })
# def feedback_view(request):
#     # Proses atau tampilkan feedback page
#     return render(request, 'session_app/feedback.html')  # Pastikan template feedback.html ada
#


# def answer_questions(request, pk):
#     feature = get_object_or_404(Feature, pk=pk)
#
#     # Membuat session baru untuk user dan fitur jika belum ada
#     session, created = Session.objects.get_or_create(checkup_group=request.user.checkup_group, feature=feature)
#
#     questions = feature.questions.prefetch_related('choices').all()
#
#     if request.method == 'POST':
#         for question in questions:
#             answer = request.POST.get(f'answer_{question.id}')
#             # Cek jika ada jawaban
#             if answer:
#                 user_response = UserResponse.objects.create(
#                     session=session,
#                     question=question,
#                     answer_text=answer if question.question_type.name == 'Essay' else None
#                 )
#                 # Untuk Multiple Choice
#                 if question.question_type.name == 'Multiple Choice':
#                     selected_choices = request.POST.getlist(f'choices_{question.id}')
#                     user_response.multiple_choice_answers.set(selected_choices)
#
#         return redirect('feedback')  # Setelah menyimpan, arahkan ke halaman feedback
#
#     return render(request, 'session_app/answer_questions.html', {'feature': feature, 'questions': questions})


