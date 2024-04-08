# models.py

from django.db import models
from django.utils import timezone
import uuid

class SearchLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    search_request = models.JSONField()
    search_response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.TextField(default="BGG")

    def __str__(self):
        return str(self.id)

class APIMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class APIMethodModifier(models.Model):
    method = models.ForeignKey(APIMethod, on_delete=models.CASCADE, related_name="modifiers")
    modifier_name = models.CharField(max_length=100)
    modifier_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.method.name} - {self.modifier_name}"

class Game(models.Model):
    game_id = models.IntegerField(unique=True)
    game_name = models.CharField(max_length=200)

    def __str__(self):
        return self.game_name

class NounChunk(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    chunks_data = models.JSONField() 
    version = models.IntegerField()

    def __str__(self):
        return f"Chunks for {self.game.game_name}"

class User(models.Model):
    username = models.CharField(max_length=100)
    games_played = models.ManyToManyField(Game, through='Play') 

    def __str__(self):
        return self.username

class Comment(models.Model):
    username = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    comment = models.TextField()
    source = models.TextField()

    def __str__(self):
        return f"{self.username} on {self.game.game_name}"

class Rating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    rating = models.FloatField()
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.rating}/10 by {self.username} for {self.game.game_name}"

class HotItem(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rank = models.IntegerField()
    date_collected = models.DateField()

    def __str__(self):
        return f"{self.game.game_name} - Rank {self.rank} on {self.date_collected}"

class Play(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the User
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  # Reference to the Game
    play_date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"{self.game.game_name} - {self.user.username} plays"

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField()
    thread_id = models.IntegerField()
    article = models.CharField(max_length = 256)
    body = models.TextField()
    
    def __str__(self):
        return self.article