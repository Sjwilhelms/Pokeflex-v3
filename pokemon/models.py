from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Pokemon(models.Model):
    pokedex_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    sprite_front = models.URLField()
    sprite_back = models.URLField(blank=True, null=True)
    sprite_artwork = models.URLField(blank=True, null=True)

    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    species = models.CharField(max_length=100, blank=True)

    types = models.JSONField(default=list)

    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()

    description = models.TextField(blank=True)

    generation = models.IntegerField(default=1)

    rarity = models.CharField(max_length=20, default='common')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pokedex_id']

    def __str__(self):
        return f"#{self.pokedex_id:03d} {self.name.title()}"

    @property
    def total_stats(self):
        return self.hp + self.attack + self.defense + self.special_attack + self.special_defense + self.speed

    @property
    def height_meters(self):
        return self.height / 10

    @property
    def weight_kg(self):
        return self.weight / 10


class UserPokemonDiscovery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    first_seen = models.DateTimeField(auto_now_add=True)
    times_seen = models.IntegerField(default=1)
    times_guessed_correctly = models.IntegerField(default=0)

    fastest_guess_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ['user', 'pokemon']

    def __str__(self):
        return f"{self.user.username} - {self.pokemon.name}"


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    session_duration = models.IntegerField(default=60)

    pokemon_encountered = models.ManyToManyField(Pokemon, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['started_at']

    def __str__(self):
        return f"Session {self.id}: {self.score}/{self.total_questions}"

    @property
    def accuracy(self):
        if self.total_questions == 0:
            return 0
        return (self.score / self.total_questions) * 100


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    total_pokemon_discovered = models.IntegerField(default=0)
    total_games_played = models.IntegerField(default=0)
    highest_score = models.IntegerField(default=0)
    total_playtime = models.IntegerField(default=0)

    discovery_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def update_discovery_percentage(self):
        total_pokemon = Pokemon.objects.count()
        if total_pokemon > 0:
            discovered = UserPokemonDiscovery.objects.filter(user=self.user).count()
            self.discovery_percentage = (discovered / total_pokemon) * 100
            self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
