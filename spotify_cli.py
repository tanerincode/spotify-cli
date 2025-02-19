#!/usr/bin/env python3
import os
import click
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env
# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the .env path dynamically
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    click.echo("⚠️ Warning: .env file not found! Ensure it's in the same directory as spotify_cli.py")


# Spotify API Credentials (from .env file)
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-modify-public"
))

@click.group()
def cli():
    """Spotify CLI Application"""
    pass

@click.command()
@click.argument("playlist_name")
@click.option("--description", default="A playlist created via CLI", help="Playlist description")
def create_playlist(playlist_name, description):
    """Create a new Spotify playlist"""
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=description)
    click.echo(f"✅ Playlist '{playlist_name}' created successfully! 🎶")
    click.echo(f"🔗 Link: {playlist['external_urls']['spotify']}")

@click.command()
@click.argument("playlist_name")
@click.argument("songs_file", type=click.File("r"))
def add_songs(playlist_name, songs_file):
    """Add songs from a file to a Spotify playlist, preventing duplicates"""
    user_id = sp.me()["id"]

    # Find the playlist by name
    playlists = sp.user_playlists(user_id)["items"]
    playlist = next((p for p in playlists if p["name"] == playlist_name), None)
    if not playlist:
        click.echo("❌ Playlist not found!")
        return

    playlist_id = playlist["id"]

    # Get existing tracks in the playlist
    existing_tracks = set()
    results = sp.playlist_tracks(playlist_id)
    for item in results["items"]:
        existing_tracks.add(item["track"]["id"])

    track_uris = []

    # Read songs from file and search
    for line in songs_file:
        song = line.strip()
        result = sp.search(q=song, limit=1, type="track")
        if result["tracks"]["items"]:
            track = result["tracks"]["items"][0]
            track_id = track["id"]

            if track_id not in existing_tracks:
                track_uris.append(track["uri"])
                existing_tracks.add(track_id)  # Add it to the set to prevent re-adding in this run
                click.echo(f"🎵 Added: {song}")
            else:
                click.echo(f"⚠️ Skipped (Already in Playlist): {song}")
        else:
            click.echo(f"⚠️ Not found: {song}")

    # Add new songs to playlist
    if track_uris:
        sp.user_playlist_add_tracks(user_id, playlist_id, track_uris)
        click.echo(f"✅ Added {len(track_uris)} new songs to '{playlist_name}'!")
    else:
        click.echo("🔄 No new songs to add!")
        
@click.command()
@click.argument("playlist_name")
def cleanup(playlist_name):
    """Remove duplicate songs from a Spotify playlist"""
    user_id = sp.me()["id"]

    # Find the playlist by name
    playlists = sp.user_playlists(user_id)["items"]
    playlist = next((p for p in playlists if p["name"] == playlist_name), None)
    if not playlist:
        click.echo("❌ Playlist not found!")
        return

    playlist_id = playlist["id"]
    track_ids = []
    seen_tracks = set()

    # Get all tracks in the playlist
    results = sp.playlist_tracks(playlist_id)
    for item in results["items"]:
        track_id = item["track"]["id"]

        if track_id in seen_tracks:
            track_ids.append(track_id)  # Mark for deletion
        else:
            seen_tracks.add(track_id)  # First occurrence, keep it

    # Remove duplicates
    if track_ids:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, track_ids)
        click.echo(f"✅ Removed {len(track_ids)} duplicate songs from '{playlist_name}'!")
    else:
        click.echo("🎵 No duplicates found, playlist is clean!")

cli.add_command(create_playlist)
cli.add_command(add_songs)
cli.add_command(cleanup)

if __name__ == "__main__":
    cli()