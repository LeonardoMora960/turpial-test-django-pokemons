from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from pokemon import views

urlpatterns = [
    # Login
    path('login/', views.Login.as_view()),

    # Pokemon Specie Detail V
    path('pokemons/<int:pk>/', views.PokemonSpecieDetail.as_view()),

    # Pokemon Storage, Pokemon catch
    path('pokemons/own/', views.PokemonStorageAndCatch.as_view(), name="pokemons_own"),

    # Pokemon rename, Pokemon release
    path('pokemons/own/<int:pk>/', views.PokemonRenameAndRelease.as_view()),

    # Pokemon party
    path('pokemons/own/party/', views.PokemonParty.as_view()),

    # Swap party member
    path('pokemons/own/swap/', views.PokemonSwapParty.as_view()),

    # Regions list V
    path('regions/', views.RegionsList.as_view()),

    # Regions detail V
    path('regions/<int:pk>/', views.RegionsDetail.as_view()),

    # Location detail V
    path('location/<int:pk>/', views.LocationsDetail.as_view()),

    # Area detail V
    path('areas/<int:pk>/', views.AreasDetail.as_view()),


    # set data areas
    path('areas/', views.AreasList.as_view()),

    # Set data Locations
    path('location/', views.LocationList.as_view()),

    # Set data pokemons
    path('pokemons/', views.SpeciesList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)