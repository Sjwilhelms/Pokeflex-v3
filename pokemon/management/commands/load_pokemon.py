import requests
import time
from django.core.management.base import BaseCommand
from pokemon.models import Pokemon


class Command(BaseCommand):
    help = 'Load Pokemon data from PokeAPI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            type=int,
            default=1,
            help='Starting Pokemon ID (default: 1)'
        )
        parser.add_argument(
            '--end',
            type=int,
            default=151,
            help='Ending Pokemon ID (default: 151 for Gen 1)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing Pokemon'
        )

    def handle(self, *args, **options):
        start_id = options['start']
        end_id = options['end']
        force_update = options['force']

        self.stdout.write(f"Loading Pokemon {start_id} to {end_id}...")

        for pokemon_id in range(start_id, end_id + 1):
            try:
                # Check if Pokemon already exists
                if not force_update and Pokemon.objects.filter(pokedex_id=pokemon_id).exists():
                    self.stdout.write(f"Pokemon #{pokemon_id} already exists, skipping...")
                    continue

                self.stdout.write(f"Fetching Pokemon #{pokemon_id}...")

                # Fetch Pokemon data
                pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
                if pokemon_response.status_code != 200:
                    self.stdout.write(
                        self.style.WARNING
                        (f"Failed to fetch Pokemon #{pokemon_id}")
                    )
                    continue

                pokemon_data = pokemon_response.json()

                # Fetch species data for description and species name
                species_response = requests.get(pokemon_data['species']['url'])
                species_data = species_response.json() if species_response.status_code == 200 else {}

                # Extract types
                types = [t['type']['name'] for t in pokemon_data['types']]

                # Extract stats
                stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}

                # Get English description
                description = ''
                if species_data and 'flavor_text_entries' in species_data:
                    english_entries = [
                        entry for entry in species_data['flavor_text_entries']
                        if entry['language']['name'] == 'en'
                    ]
                    if english_entries:
                        description = english_entries[0]['flavor_text'].replace('\f', ' ').replace('\n', ' ')

                # Get species (genus)
                species_name = ''
                if species_data and 'genera' in species_data:
                    english_genus = [
                        genus for genus in species_data['genera']
                        if genus['language']['name'] == 'en'
                    ]
                    if english_genus:
                        species_name = english_genus[0]['genus']

                # Create or update Pokemon
                pokemon, created = Pokemon.objects.update_or_create(
                    pokedex_id=pokemon_id,
                    defaults={
                        'name': pokemon_data['name'],
                        'sprite_front': pokemon_data['sprites']['front_default'] or '',
                        'sprite_back': pokemon_data['sprites']['back_default'] or '',
                        'sprite_artwork': pokemon_data['sprites']['other']['official-artwork']['front_default'] or '',
                        'height': pokemon_data['height'],
                        'weight': pokemon_data['weight'],
                        'species': species_name,
                        'types': types,
                        'hp': stats.get('hp', 0),
                        'attack': stats.get('attack', 0),
                        'defense': stats.get('defense', 0),
                        'special_attack': stats.get('special-attack', 0),
                        'special_defense': stats.get('special-defense', 0),
                        'speed': stats.get('speed', 0),
                        'description': description,
                        'generation': 1,  # Gen 1 for now
                    }
                )

                action = "Created" if created else "Updated"
                self.stdout.write(
                    self.style.SUCCESS(f"{action} {pokemon}")
                )

                # Be nice to the API
                time.sleep(0.1)

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error processing Pokemon #{pokemon_id}: {e}")
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f"Finished loading Pokemon {start_id} to {end_id}")
        )
