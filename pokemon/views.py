from pokemon.models import *
from pokemon.serializers import *
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

# Authentication Login with Token
class Login(APIView):

    def post(self, request, *args, **kwargs):

        if request.data['username'] is None or request.data['password'] is None:
            return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=request.data['username'], password=request.data['password'])

        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

        token,_ = Token.objects.get_or_create(user = user)

        if token:
            login(self.request, user)
            return Response({'token': str(token)})

# Get and set data list species pokémons
class SpeciesList(generics.ListCreateAPIView):
    queryset = Species.objects.none()
    serializer_class = SpeciesSerializer

    def get_queryset(self):
         queryset = Species.objects.all()
         return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Species.objects.all()
        output_serializer = SpeciesSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

# Get data specie pokémon by id
class PokemonSpecieDetail(generics.RetrieveAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer

# Get data region by id
class RegionsDetail(generics.RetrieveAPIView):
    queryset = Regions.objects.all()
    serializer_class = RegionsLocationsSerializer

# Get data list regions
class RegionsList(generics.ListCreateAPIView):
    queryset = Regions.objects.none()
    serializer_class = RegionsSerializer

    def get_queryset(self):
         queryset = Regions.objects.all()
         return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Regions.objects.all()
        output_serializer = RegionsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

# Get and set data list location 
class LocationList(generics.ListCreateAPIView):
    queryset = Locations.objects.none()
    serializer_class = LocationsSerializer

    def get_queryset(self):
         queryset = Locations.objects.all()
         return queryset

    def create(self, request, *args, **kwargs):
        for location_list in request.data:
            location_list['region'] = Regions.objects.filter(name = location_list['region']).values_list('id')[0][0]

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Locations.objects.all()
        output_serializer = LocationsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

# Get data location by id
class LocationsDetail(generics.RetrieveAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

# Get and set data list areas
class AreasList(generics.ListCreateAPIView):
    queryset = Areas.objects.none()
    serializer_class = AreasListSerializer
    locations = Locations.objects.all()

    def get_queryset(self):
         queryset = Areas.objects.all()
         return queryset

    def create(self, request, *args, **kwargs):

        for area_list in request.data:
            area_list['location'] = Locations.objects.filter(name = area_list['location']).values()[0]['id']

        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        for response_area in serializer.data:
            for area_list in request.data:
                if(response_area['name'] == area_list['name']):
                    area_selected = area_list

            for species_list in area_selected['pokemons']:
                species = Species.objects.filter(name = species_list.capitalize()).values()[0]['id']
                species = Species.objects.get(id=species)
                areas = Areas.objects.get(id=response_area['id'])

                species.areas.add(areas)

        results = Areas.objects.all()
        output_serializer = AreasListSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

# Get data area by id
class AreasDetail(generics.RetrieveAPIView):
    queryset = Areas.objects.all()
    serializer_class = AreasSerializer

# Get and Set data storage pokémons by user
class PokemonStorageAndCatch(generics.ListCreateAPIView):
    queryset = Storage_Users.objects.filter()
    serializer_class = StoragePokemonsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        is_member_party = 0 if request.data['is_party_member'] else 1
        members_party = Storage_Users.objects.filter(is_party_member = True, user = request.user.id)

        if ((is_member_party + len(members_party)) >= 6):
            request.data['is_party_member'] = False

        serializer = CatchPokemonsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        results = Storage_Users.objects.filter(id=serializer.data['id'])
        output_serializer = CatchPokemonsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        results = Storage_Users.objects.filter(user = request.user.id)
        output_serializer = StoragePokemonsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

# Update name and deleted pokémon of storage by user
class PokemonRenameAndRelease(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage_Users.objects.all()
    serializer_class = StoragePokemonsDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        results = Storage_Users.objects.filter(user = request.user.id)
        output_serializer = StoragePokemonsDetailsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

# Get data pokémon storage party by user
class PokemonParty(generics.ListAPIView):
    queryset = Storage_Users.objects.filter(is_party_member = True)
    serializer_class = StoragePokemonsSerializer
    permission_classes     = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        results = Storage_Users.objects.filter(is_party_member = True, user = request.user.id)
        output_serializer = StoragePokemonsDetailsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)

# Update members of the party by user
class PokemonSwapParty(generics.CreateAPIView):
    queryset = Storage_Users.objects.filter(is_party_member = True)
    serializer_class = StoragePokemonsSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        members_party   = Storage_Users.objects.filter(is_party_member = True, user = request.user.id)
        update_data    = []
        leaving_party  = []
        entering_party = None 

        if(request.data['leaving_the_party'] is not None):
            leaving_party   = Storage_Users.objects.filter(
                id = request.data['leaving_the_party'],  
                user = request.user.id).values()
            if(leaving_party):
                leaving_party   = {'id': leaving_party[0]['id'],  'is_party_member' : False}
                update_data.append(leaving_party)

        if(request.data['entering_the_party'] is not None):
            entering_party   = Storage_Users.objects.filter(
                id = request.data['entering_the_party'],  
                user = request.user.id).values()
            if(entering_party  is not None):
                entering_party = {'id': entering_party[0]['id'], 'is_party_member' : True}

        if ((len(members_party) - len(leaving_party) ) >= 6 and entering_party is not None):
            entering_party['is_party_member'] = False
            update_data.append(entering_party)
        else:
            update_data.append(entering_party)

        for swap_party in update_data:
            if(swap_party is not None):
                serializer = StorageSwapPokemonsDetailsSerializer(data=swap_party, partial=True)
                serializer.is_valid(raise_exception=True)
                data_update, created = Storage_Users.objects.update_or_create(id=swap_party['id'],  defaults={"is_party_member" : swap_party['is_party_member']})
                setattr(data_update, 'is_party_member', swap_party['is_party_member'])
                data_update.save()
            
        results = Storage_Users.objects.filter(is_party_member=True, user=request.user.id)
        output_serializer = StoragePokemonsSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data)
