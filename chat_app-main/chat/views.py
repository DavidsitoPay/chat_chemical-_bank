from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime

min_aware = make_aware(datetime.min)



@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id)

    # Obtener los mensajes de chat con el usuario de la sala
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))

    chats = chats.order_by('timestamp') 

    # Lista de usuarios con su último mensaje
    user_last_messages = []
    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

        user_last_messages.sort(
            key=lambda x: x['last_message'].timestamp if x['last_message'] and x['last_message'].timestamp else min_aware,
            reverse=True
        )


    # Manejo del envío de mensajes (POST)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        file = request.FILES.get('file')

        try:
            receiver = User.objects.get(username=room_name)
        except User.DoesNotExist:
            receiver = None

        if receiver and (content or file):
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                file=file if file else None
            )
            return redirect('chat', room_name=room_name)

    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })
