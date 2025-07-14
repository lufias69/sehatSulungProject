from django.shortcuts import render, redirect
from django.http import JsonResponse
from fastapi.encoders import jsonable_encoder

from .models import HealthPredictionResult  # Pastikan model sudah ada
from session_app.models import Session, UserResponse
# Import fungsi prediksi_kesehatan dari geminiAPI.py
from django.contrib.auth.decorators import login_required

from .tools.geminiAPI import prediksi_kesehatan, api_keys


@login_required
def make_health_prediction(request, session_id):

    session = Session.objects.get(id=session_id)

    if not session.feature.requires_analysis:
        return JsonResponse({'error': 'Feature requires analysis.'}, status=400)

    print(f"Session: {session.feature.requires_analysis}")
    umur = session.checkup_group.get_umur_terformat()
    kategori = session.checkup_group.kategori.nama_kategori

    # initial_instructions = session.feature.initial_instructions
    # print(f"Initial Instructions: {initial_instructions}")
    # final_instructions = session.feature.final_instructions

    # print(f"Final Instructions: {final_instructions}")


    # Ambil UserResponses yang terkait dengan session ini
    user_responses = UserResponse.objects.filter(session=session)
    jawaban_all = {}
    for response in user_responses:
        pertanyan = response.question.question_text

        if response.answer_text:
            jawaban_essai = response.answer_text
            # print(f"Jawaban Esaiiiii: {jawaban_essai}")
            jawaban_all[pertanyan] = jawaban_essai
            # print(f"Jawaban All: {jawaban_all}")
            continue
            # jawaban_all.append(jawaban_essai)
        if response.multiple_choice_answers.all:
            jawaban_multiple_choice = response.multiple_choice_answers.all()

            jawaban_multiple_choice_text = ""
            for choice in jawaban_multiple_choice:
                # print(f"Pertanyaan: {pertanyan}, Jawaban: {choice.choice_text}")
                jawaban_multiple_choice_text += f"{choice.choice_text} "
                # jawaban_all.append(jawaban_multiple_choice_text)
            jawaban_all[pertanyan] = f"{jawaban_multiple_choice_text}"

    # print(f"Jawaban All: {jawaban_all}")

            # print(f"Jawaban Multiple Choice: {jawaban_multiple_choice}")
            # jawaban_all.append(jawaban_multiple_choice)
        # print(f"Pertanyaan: {pertanyan}, Jawaban: {jawaban_multiple_choice}")

    data_pasien = f"Umur: {umur}"
    deskripsi_kasus = jawaban_all
    initial_instructions = session.feature.initial_instructions
    final_instructions = session.feature.final_instructions
    # print(f"Deskripsi Kasus: {data_pasien}")
    # print(f"Deskripsi Kasus: {deskripsi_kasus}")



    # Memanggil fungsi prediksi_kesehatan untuk mendapatkan hasil prediksi
    prediction_result = prediksi_kesehatan(
        api_keys=api_keys,
        data_pasien=data_pasien,
        deskripsi_kasus=deskripsi_kasus,
        instruksi_awal=initial_instructions,
        instruksi_akhir=final_instructions
    )
    print()
    print(f"Hasil Prediksi: {prediction_result}")
    #
    if 'error' in prediction_result:
        # Jika ada error, kembalikan error ke user
        return JsonResponse({'error': prediction_result['error']}, status=400)

    # Ambil hasil prediksi
    health_recommendation = prediction_result.rekomendasi_kesehatan
    criteria_details = prediction_result.detail_kriteria

    # Simpan hasil prediksi ke dalam database (model HealthPredictionResult)
    try:
        session = Session.objects.get(id=session_id)


        health_prediction_result = HealthPredictionResult.objects.create(
            session=session,
            health_recommendation=health_recommendation,
            criteria_details=jsonable_encoder(criteria_details)
        )
        return redirect('session_app:feedback', checkup_group_id=session.checkup_group.id, session_id=session.id)
        # Tampilkan hasil prediksi kepada user (atau arahkan ke halaman lain)
        # return JsonResponse({
        #     'health_recommendation': {},#health_recommendation,
        #     'criteria_details': {}#criteria_details
        # })

    except Session.DoesNotExist:
        return JsonResponse({'error': 'Session not found.'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid request method. Please use POST.'}, status=405)
