from rest_framework import serializers
from pokemon.models import *
from django.contrib.auth.models import User

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta: 
        model  = Species 
        fields = ('__all__')
        extra_kwargs = {'areas': {'write_only':True}}

class SpecieDetailsSerializer(serializers.ModelSerializer):
    class Meta: 
        model  = Species 
        fields = ('id', 'name', 'sprites')

class RegionsSerializer(serializers.ModelSerializer):
    class Meta: 
        model  = Regions 
        fields = ('__all__')

class LocationsSerializer(serializers.ModelSerializer):

    class Areas(serializers.ModelSerializer):
        pokemon_count  = serializers.IntegerField(read_only=True, source='species.count')
        
        class Meta: 
            model  = Areas 
            fields = ('id','name','pokemon_count', 'location')
        
        def get_pokemon_count(self, obj):
            return obj.pokemons.__len__()

    areas = Areas(many=True, read_only=True)
    class Meta: 
        model  = Locations 
        fields = ('id', 'name', 'region', 'areas')

class SpeciesAreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('id','name','sprites')

class AreasSerializer(serializers.ModelSerializer):
    pokemons       = SpeciesAreasSerializer(read_only=True, many=True, source='species')
    pokemon_count  = serializers.IntegerField(read_only=True, source='species.count')
    class Meta: 
        model  = Areas 
        fields = ('id','name', 'pokemons', 'pokemon_count', 'location')

class RegionsLocationsSerializer(serializers.ModelSerializer):
    
    class Locations(serializers.ModelSerializer):
        class Meta: 
            model = Locations 
            fields = ('id', 'name')

    locations = Locations(many=True, read_only=True)
    class Meta: 
        model = Regions 
        fields = ('id', 'name', 'locations')

class AreasListSerializer(serializers.ModelSerializer):
    class Meta: 
        model  = Areas 
        fields = ('id', 'name', 'location')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('username','password')

class StoragePokemonsSerializer(serializers.ModelSerializer):
    specie = SpecieDetailsSerializer(read_only=True)
    class Meta:
        model = Storage_Users
        fields = ('id', 'nick_name', 'is_party_member', 'specie')

class CatchPokemonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage_Users
        fields = ('id', 'nick_name', 'is_party_member', 'specie', 'user')
        extra_kwargs = {'user': {'write_only': True}}

class StoragePokemonsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage_Users
        fields = ('id', 'nick_name', 'is_party_member','specie')
        extra_kwargs = {
            'id': {'read_only' : True}, 
            'is_party_member': {'read_only': True},
            'specie': {'read_only':  True}
        }


class StorageSwapPokemonsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage_Users
        fields = ('id', 'nick_name', 'is_party_member','specie')
        extra_kwargs = {
            'id': {'read_only' : True}, 
            'nick_name': {'read_only': True},
            'specie': {'read_only':  True}
        }
    
