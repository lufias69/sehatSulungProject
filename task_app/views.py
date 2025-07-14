# task_app/views.py
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from fitur_app.models import CheckupGroup, Feature
# from task_app.models import Task, TaskCompletion
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone

from session_app.models import Session, UserResponse
from .models import Task

from django.shortcuts import render
from fitur_app.models import CheckupGroup
from task_app.models import Task
from datetime import timedelta
from django.utils import timezone

# task_app/views.py
from django.shortcuts import render
from fitur_app.models import CheckupGroup

def checkup_group_list(request):
    # Mengambil CheckupGroup yang dimiliki oleh pengguna yang sedang login
    print(request.user)

    if request.user.is_authenticated:
        print("authenticated")
    else:
        return HttpResponseRedirect('/accounts/login')
    try:
        checkup_groups = CheckupGroup.objects.filter(user=request.user, is_deleted=False)
        print(checkup_groups)
        checkup_group_ids = list(checkup_groups.values_list('id', flat=True))  # Convert to list if needed
        # print(checkup_group_ids)
        tasks = Task.objects.all()
        # print(tasks)
            # print(fitur.id)
        print("-"*20)
        task_show = []
        for task in tasks:
            # print(f"Task: {task.name}")
            features = task.features.all()  # Retrieve all related features for each task
            # print(f"- {feature_task.id}")
            # print("Associated Features:")
            for feature_task in features:
                for group_id in checkup_group_ids:
                    group = CheckupGroup.objects.get(id=group_id)
                    fitur = group.get_relevant_features()
                    for feature in fitur:
                        if feature.id == feature_task.id:
                            print(f"Task: {task.name}, group_id:{group_id}, feature.id:{feature.id}, feature.name{feature.name}")
                            if not Session.objects.filter(checkup_group=group_id).order_by(
                                '-created_at').first():
                                Fitur_selected = Feature.objects.get(id=feature.id)
                                task_show.insert(0,{'status': "task",
                                 'feature_selected':Fitur_selected,
                                 'checkupGroup':group,
                                 'feature_id':feature.id
                                 })
                                # pada dictionary beri tanda bahwa ada task

                                print(f"Fitur_selected:{Fitur_selected},CheckupGroup: {group}")  # simpan dalam distionary untuk dijadikan contex
                                print(
                                    f"feature.id:{feature.id}, group_id:{group_id}")  # simpan dalam distionary untuk dijadikan contex
                                print("tidak ada session")
                                continue
                            latest_session = Session.objects.filter(checkup_group=group_id).order_by(
                                '-created_at').first()
                            # print(f"Sessions: {latest_session.created_at}")
                            time_difference = timezone.now() -  latest_session.created_at
                            # Convert the time difference to total days (including partial days)
                            total_days = time_difference.days + time_difference.seconds / (60 * 60 * 24)
                            print(f"Time difference: {total_days}")
                            print(f"Task duration: {task.task_duration}")
                            if task.task_duration <= total_days:
                                #pada dictionary beri tanda bahwa ada task
                                Fitur_selected = Feature.objects.get(id=feature.id)
                                # print(f"Fitur_selected:{Fitur_selected},CheckupGroup: {group}") #simpan dalam distionary untuk dijadikan contex
                                # print(f"feature.id:{feature.id}, group_id:{group_id}") #simpan dalam distionary untuk dijadikan contex

                                task_show.insert(0,{'status': "task",
                                                  'feature_selected': Fitur_selected,
                                                  'checkupGroup': group,
                                                  'feature_id': feature.id
                                                  })
                            else:
                                Fitur_selected = Feature.objects.get(id=feature.id)
                                # user_response = UserResponse.objects.get(id=latest_session.id)
                                #pada dictionary beri tanda bahwa tidak ada task
                                task_show.append({'status': "no task",
                                                  'feature_selected': Fitur_selected,
                                                  'checkupGroup': group,
                                                  'feature_id': feature.id,
                                                  'latest_session':latest_session,
                                                  # 'user_responses':user_response
                                                  })
                                # print("ambil last session", latest_session) #simpan dalam distionary untuk dijadikan contex
                                # print("user respone", user_response)
                                # print(group_id, feature.id, feature.name)
                            # path('feature/<int:pk>/answer/<int:checkup_group_id>/', views.answer_questions,
                            #      name='answer_questions'),
                            print()

        print(task_show)
        task_data_list = task_show
    except CheckupGroup.DoesNotExist:
        task_show = []
        task_data_list = task_show

    return render(request, 'task_app/checkup_group_list.html', {'task_data_list':task_data_list})

from django.shortcuts import render
from django.utils import timezone
from task_app.models import Task
from fitur_app.models import CheckupGroup
from fitur_app.models import Feature
from session_app.models import Session


# def checkup_group_list(request):
#     # Retrieve all tasks
#     tasks = Task.objects.all()
#
#     checkup_group_ids = [group.id for group in CheckupGroup.objects.filter(user=request.user, is_deleted=False)]
#     tasks_status = []  # To store information about tasks and features
#
#     # Loop through each task and check whether the task has been completed or is due
#     for task in tasks:
#         task_data = {
#             'task_name': task.name,
#             'task_duration': task.task_duration,
#             'features': []
#         }
#
#         features = task.features.all()  # Retrieve all related features for each task
#
#         for feature_task in features:
#             for group_id in checkup_group_ids:
#                 group = CheckupGroup.objects.get(id=group_id)
#                 fitur = group.get_relevant_features()
#
#                 for feature in fitur:
#                     if feature.id == feature_task.id:
#                         # Get the latest session for the CheckupGroup
#                         latest_session = Session.objects.filter(checkup_group=group_id).order_by('-created_at').first()
#
#                         if latest_session:
#                             time_difference = timezone.now() - latest_session.created_at
#                             # Convert the time difference to total days (including partial days)
#                             total_days = time_difference.days + time_difference.seconds / (60 * 60 * 24)
#
#                             # Check if the task duration has passed
#                             if task.task_duration <= total_days:
#                                 task_status = 'pending'
#                             else:
#                                 task_status = 'completed'
#
#                             # Add the information to the dictionary
#                             task_data['features'].append({
#                                 'feature_id': feature.id,
#                                 'feature_name': feature.name,
#                                 'task_status': task_status,
#                                 'last_session': latest_session.created_at,
#                                 'time_difference': total_days
#                             })
#
#         tasks_status.append(task_data)
#
#     return render(request, 'task_app/checkup_group_list.html', {
#         'tasks_status': tasks_status  # Pass the tasks data to the context
#     })


@login_required
def task_list(request):
    # Ambil semua task
    tasks = Task.objects.all()

    return render(request, 'task_app/task_list.html', {'tasks': tasks})
# def task_list(request):
#     # Mendapatkan CheckupGroup yang dimiliki oleh user
#     checkup_groups = CheckupGroup.objects.filter(user=request.user, is_deleted=False)
#
#     tasks_to_show = []  # Daftar tugas yang akan ditampilkan ke user
#
#     for group in checkup_groups:
#         # Mendapatkan tasks yang terkait dengan CheckupGroup
#         tasks = Task.objects.filter(checkup_group=group)
#
#         for task in tasks:
#             # Ambil waktu session terakhir
#             last_session = group.sessions.last()  # Ambil sesi terakhir yang diadakan oleh CheckupGroup
#
#             if last_session:
#                 last_completed = last_session.created_at
#
#                 # Menghitung perbedaan waktu antara sekarang dan waktu sesi terakhir
#                 time_difference = timezone.now() - last_completed
#
#                 # Cek apakah task belum diselesaikan dalam rentang waktu yang sesuai
#                 if time_difference >= timedelta(days=task.task_duration):  # Jika waktu lebih dari durasi task
#                     tasks_to_show.append(task)  # Menambahkan task yang perlu diselesaikan
#
#     return render(request, 'task_app/task_list.html', {
#         'tasks_to_show': tasks_to_show,
#     })

# def task_list(request):
#     # Mendapatkan CheckupGroup yang dimiliki oleh user
#     checkup_groups = CheckupGroup.objects.filter(user=request.user, is_deleted=False)
#
#     # Menyaring tugas yang terkait dengan CheckupGroup dan belum diselesaikan
#     tasks_to_show = []
#     for group in checkup_groups:
#         tasks = Task.objects.filter(feature__in=[feature for feature in group.features.all()])
#
#         # Periksa apakah task sudah dikerjakan dalam rentang waktu tertentu
#         for task in tasks:
#             task_completion = TaskCompletion.objects.filter(user=request.user, task=task, checkup_group=group)
#
#             # Cek apakah task sudah dikerjakan atau belum
#             if task_completion.exists():
#                 last_completed = task_completion.latest('completed_at')
#                 # Jika sudah dikerjakan, periksa waktu task
#                 if task.task_time == 'daily' and last_completed.completed_at > timezone.now() - timedelta(days=1):
#                     continue  # Task sudah dikerjakan dalam 24 jam terakhir
#                 elif task.task_time == 'weekly' and last_completed.completed_at > timezone.now() - timedelta(weeks=1):
#                     continue  # Task sudah dikerjakan dalam 7 hari terakhir
#                 elif task.task_time == 'monthly' and last_completed.completed_at > timezone.now() - timedelta(weeks=4):
#                     continue  # Task sudah dikerjakan dalam 30 hari terakhir
#             tasks_to_show.append(task)
#
#     return render(request, 'task_app/task_list.html', {
#         'tasks_to_show': tasks_to_show,
#     })
# task_app/views.py

from django.shortcuts import redirect
# from task_app.models import TaskCompletion
# from django.utils import timezone

# @login_required
# def answer_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#
#     # Simpan TaskCompletion setelah menyelesaikan task
#     TaskCompletion.objects.create(
#         user=request.user,
#         task=task,
#         checkup_group=CheckupGroup.objects.first(),  # Sesuaikan dengan CheckupGroup yang relevan
#         completed_at=timezone.now()
#     )
#
#     return redirect('task_app:task_list')  # Redirect ke halaman task list


# task_app/views.py

from django.shortcuts import render, redirect
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_app:task_list')  # Redirect ke halaman daftar task setelah menyimpan
    else:
        form = TaskForm()

    return render(request, 'task_app/create_task.html', {'form': form})

# task_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_app:task_list')  # Setelah edit, arahkan ke halaman task list
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_app/edit_task.html', {'form': form, 'task': task})


# task_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('task_app:task_list')  # Setelah dihapus, arahkan ke halaman task list

    return render(request, 'task_app/confirm_delete_task.html', {'task': task})
