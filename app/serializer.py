from rest_framework.serializers import ModelSerializer
from .models import Person, Message, Conversations

class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
    
class ConversationsSerializer(ModelSerializer):
    class Meta:
        model = Conversations
        fields = '__all__'