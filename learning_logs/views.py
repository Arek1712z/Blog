from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """Main page for app Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Showing all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Shows one topic and displays related entries"""
    topic = Topic.objects.get(id=topic_id)
    # Checking it topic owns to current user
    check_topic_owner(request, topic)
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add new topic"""
    if request.method != 'POST':
        # No data provided, create a blank form.
        form = TopicForm()
    else:
        # The data has been provided by request POST, it must be processed.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # Display blank form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Adding new entry for definite topic"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        # No data provided, create a blank form.
        form = EntryForm()
    else:
        # The data has been provided by request POST, it must be processed.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Display blank form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Editing an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        #Initial request, filling in the form with the current content of the entry.
        form = EntryForm(instance=entry)
    else:
        # Data has been provided by request POST, it must be processed.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_topic_owner(request, topic):
    if topic.owner != request.user:
        raise Http404