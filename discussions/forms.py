from django.forms import ModelForm
from discussions.models import Discussions


class DiscussionCreateForm(ModelForm):

    class Meta:
        model = Discussions
        fields = ('title', 'content')
        