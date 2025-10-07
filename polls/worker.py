import threading, queue, time
from django.db import transaction, IntegrityError
vote_queue = queue.Queue()
_worker_thread = None
_started = False
def enqueue_vote(payload):
    vote_queue.put(payload)
def _process_item(item):
    from .models import Session, Question, Option, Vote
    try:
        session = Session.objects.get(id=item['session_id'])
        question = Question.objects.get(id=item['question_id'], session=session)
        option = Option.objects.get(id=item['option_id'], question=question)
    except Exception as e:
        return
    # create Vote if not exists (unique_together ensures single vote)
    try:
        with transaction.atomic():
            Vote.objects.create(session=session, question=question, option=option, participant_id=item['participant_id'])
            # increment denormalized counter
            option.votes = option.votes + 1
            option.save(update_fields=['votes'])
    except IntegrityError:
        # duplicate vote; ignore
        return
def _worker_loop():
    while True:
        item = vote_queue.get()
        try:
            _process_item(item)
        except Exception:
            pass
        vote_queue.task_done()
def start_worker():
    global _worker_thread, _started
    if _started:
        return
    _started = True
    t = threading.Thread(target=_worker_loop, daemon=True)
    t.start()
    _worker_thread = t
