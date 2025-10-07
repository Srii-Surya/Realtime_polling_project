from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import PollSession, Question, Option, Vote
from .serializers import PollSessionSerializer, QuestionSerializer, OptionSerializer
from django.shortcuts import get_object_or_404

# Organizer creates a poll session
class CreatePollSessionView(generics.CreateAPIView):
    serializer_class = PollSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

# Start / Stop session
from rest_framework.decorators import api_view

@api_view(['PATCH'])
def start_stop_session(request, pk):
    session = get_object_or_404(PollSession, pk=pk, organizer=request.user)
    session.is_active = not session.is_active
    session.save()
    return Response({'is_active': session.is_active})

# Participant joins via join_code
@api_view(['GET'])
def join_session(request, join_code):
    session = get_object_or_404(PollSession, join_code=join_code, is_active=True)
    serializer = PollSessionSerializer(session)
    return Response(serializer.data)

# Submit vote
@api_view(['POST'])
def vote(request):
    session_id = request.data.get('session_id')
    question_id = request.data.get('question_id')
    option_id = request.data.get('option_id')
    voter_id = request.data.get('voter_id')

    # Prevent duplicate votes
    if Vote.objects.filter(question_id=question_id, voter_id=voter_id).exists():
        return Response({'detail': 'Already voted'}, status=status.HTTP_400_BAD_REQUEST)

    vote = Vote.objects.create(
        session_id=session_id,
        question_id=question_id,
        option_id=option_id,
        voter_id=voter_id
    )
    option = vote.option
    option.votes += 1
    option.save()
    return Response({'detail': 'Vote submitted'}, status=status.HTTP_202_ACCEPTED)

# Fetch results
@api_view(['GET'])
def poll_results(request, session_id):
    session = get_object_or_404(PollSession, pk=session_id)
    serializer = PollSessionSerializer(session)
    return Response(serializer.data)
