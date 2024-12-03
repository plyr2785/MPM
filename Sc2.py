import os
from tinytag import TinyTag

class Song:
    def __init__(self, title, artist, album, filepath):
        self.title = title
        self.artist = artist
        self.album = album
        self.filepath = filepath
        self.next = None

class MusicOrganizer:
    def __init__(self):
        self.head = None
        self.size = 0
        self.albums = {}

    def add_song(self, title, artist, album, filepath):
        new_song = Song(title, artist, album, filepath)
        
        # Add to LinkedList
        if not self.head:
            self.head = new_song
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_song
        
        # Track albums separately
        if album not in self.albums:
            self.albums[album] = []
        self.albums[album].append(new_song)
        self.size += 1

    def bubble_sort_album(self, songs):
        n = len(songs)
        for i in range(n):
            for j in range(0, n-i-1):
                if songs[j].title > songs[j+1].title:
                    songs[j], songs[j+1] = songs[j+1], songs[j]

    def scan_directory(self, input_dir):
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith(('.mp3', '.m4a', '.wav', '.flac')):
                    filepath = os.path.join(root, file)
                    try:
                        # Extract metadata using TinyTag
                        tag = TinyTag.get(filepath)
                        title = tag.title or os.path.splitext(file)[0]
                        artist = tag.artist or "Unknown Artist"
                        album = tag.album or "Unknown Album"
                        self.add_song(title, artist, album, filepath)
                    except:
                        # Fallback to filename if metadata extraction fails
                        title = os.path.splitext(file)[0]
                        self.add_song(title, "Unknown Artist", "Unknown Album", filepath)

    def organize_music(self, output_dir):
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Process each album
        for album, songs in self.albums.items():
            # Create album directory
            album_dir = os.path.join(output_dir, self._sanitize_filename(album))
            if not os.path.exists(album_dir):
                os.makedirs(album_dir)

            # Sort songs within album
            self.bubble_sort_album(songs)

            # Copy files to album directory
            for song in songs:
                new_filename = f"{self._sanitize_filename(song.title)}{os.path.splitext(song.filepath)[1]}"
                destination = os.path.join(album_dir, new_filename)
                self._copy_file(song.filepath, destination)

    def _sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename.strip()

    def _copy_file(self, src, dst):
        """Copy file with error handling"""
        try:
            with open(src, 'rb') as fsrc:
                with open(dst, 'wb') as fdst:
                    fdst.write(fsrc.read())
        except Exception as e:
            print(f"Error copying {src}: {str(e)}")

    def display_organization(self):
        """Display the organized structure"""
        if not self.head:
            print("No songs found!")
            return

        print("\nOrganized Music Structure:")
        for album, songs in self.albums.items():
            print(f"\nAlbum: {album}")
            print("-" * 50)
            for song in songs:
                print(f"Title: {song.title}")
                print(f"Artist: {song.artist}")
                print("-" * 30)

def main():
    organizer = MusicOrganizer()
    
    # Get input and output directories
    input_dir = input("Enter path to unorganized music folder: ")
    output_dir = input("Enter path for organized music: ")
    
    print("\nScanning and organizing music files...")
    organizer.scan_directory(input_dir)
    organizer.organize_music(output_dir)
    
    print("\nOrganization complete!")
    organizer.display_organization()

if __name__ == "__main__":
    main()