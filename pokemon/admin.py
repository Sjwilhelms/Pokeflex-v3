from django.contrib import admin
from .models import Pokemon, UserPokemonDiscovery, GameSession, UserProfile

# Register your models here.


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ['pokedex_id', 'name', 'get_types', 'total_stats',
                    'generation']
    list_filter = ['generation', 'rarity']
    search_fields = ['name', 'pokedex_id']
    ordering = ['pokedex_id']
    readonly_fields = ['total_stats', 'created_at', 'updated_at']

    def get_types(self, obj):
        return ', '.join(obj.types) if obj.types else 'None'
    get_types.short_description = 'Types'


@admin.register(UserPokemonDiscovery)
class UserPokemonDiscoveryAdmin(admin.ModelAdmin):
    list_display = ['user', 'pokemon', 'times_seen', 'times_guessed_correctly',
                    'first_seen']
    list_filter = ['first_seen', 'pokemon__generation']
    search_fields = ['user__username', 'pokemon__name']
    readonly_fields = ['first_seen']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'score', 'total_questions', 'accuracy',
                    'started_at']
    list_filter = ['started_at', 'session_duration']
    search_fields = ['user__username']
    readonly_fields = ['started_at', 'accuracy']

    def accuracy(self, obj):
        return f'{obj.accuracy:.1f}%'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_pokemon_discovered', 'total_games_played',
                    'highest_score', 'discovery_percentage']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
