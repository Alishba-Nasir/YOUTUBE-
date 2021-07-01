"""A command parser class."""

import textwrap
from typing import Sequence


class CommandException(Exception):
    """A class used to represent a wrong command exception."""
    pass


class CommandParser:
    """A class used to parse and execute a user Command."""

    def __init__(self, video_player):
        self._player = video_player

    def execute_command(self, command: Sequence[str]):
        """Executes the user command. Expects the command to be upper case.
           Raises CommandException if a command cannot be parsed.
        """
        if not command:
            raise CommandException(
                "Please enter a valid command, "
                "type HELP for a list of available commands.")

        if command[0].upper() == "NUMBER_OF_VIDEOS":
            self._player.number_of_videos()

        elif command[0].upper() == "SHOW_ALL_VIDEOS":
            self._player.show_all_videos()

        elif command[0].upper() == "PLAY":
            if len(command) != 2:
                raise CommandException(
                    "Please enter PLAY command followed by video_id.")
            self._player.play_video(command[1])

        elif command[0].upper() == "PLAY_RANDOM":
            self._player.play_random_video()

        elif command[0].upper() == "STOP":
            self._player.stop_video()

        elif command[0].upper() == "PAUSE":
            self._player.pause_video()

        elif command[0].upper() == "CONTINUE":
            self._player.continue_video()

        elif command[0].upper() == "SHOW_PLAYING":
            self._player.show_playing()

        elif command[0].upper() == "CREATE_PLAYLIST":
            if len(command) != 2:
                raise CommandException(
                    "Please enter CREATE_PLAYLIST command followed by a "
                    "playlist name.")
            self._player.create_playlist(command[1])

        elif command[0].upper() == "ADD_TO_PLAYLIST":
            if len(command) != 3:
                raise CommandException(
                    "Please enter ADD_TO_PLAYLIST command followed by a "
                    "playlist name and video_id to add.")
            self._player.add_to_playlist(command[1], command[2])

        elif command[0].upper() == "REMOVE_FROM_PLAYLIST":
            if len(command) != 3:
                raise CommandException(
                    "Please enter REMOVE_FROM_PLAYLIST command followed by a "
                    "playlist name and video_id to remove.")
            self._player.remove_from_playlist(command[1], command[2])

        elif command[0].upper() == "CLEAR_PLAYLIST":
            if len(command) != 2:
                raise CommandException(
                    "Please enter CLEAR_PLAYLIST command followed by a "
                    "playlist name.")
            self._player.clear_playlist(command[1])

        elif command[0].upper() == "DELETE_PLAYLIST":
            if len(command) != 2:
                raise CommandException(
                    "Please enter DELETE_PLAYLIST command followed by a "
                    "playlist name.")
            self._player.delete_playlist(command[1])

        elif command[0].upper() == "SHOW_PLAYLIST":
            if len(command) != 2:
                raise CommandException(
                    "Please enter SHOW_PLAYLIST command followed by a "
                    "playlist name.")
            self._player.show_playlist(command[1])

        elif command[0].upper() == "SHOW_ALL_PLAYLISTS":
            self._player.show_all_playlists()

        elif command[0].upper() == "SEARCH_VIDEOS":
            if len(command) != 2:
                raise CommandException(
                    "Please enter SEARCH_VIDEOS command followed by a "
                    "search term.")
            self._player.search_videos(command[1])

        elif command[0].upper() == "SEARCH_VIDEOS_WITH_TAG":
            if len(command) != 2:
                raise CommandException(
                    "Please enter SEARCH_VIDEOS_WITH_TAG command followed by a "
                    "video tag.")
            self._player.search_videos_tag(command[1])

        elif command[0].upper() == "FLAG_VIDEO":
            if len(command) == 3:
                self._player.flag_video(command[1], command[2])
            elif len(command) == 2:
                self._player.flag_video(command[1])
            else:
                raise CommandException(
                    "Please enter FLAG_VIDEO command followed by a "
                    "video_id and an optional flag reason.")

        elif command[0].upper() == "ALLOW_VIDEO":
            if len(command) != 2:
                raise CommandException(
                    "Please enter ALLOW_VIDEO command followed by a "
                    "video_id.")
            self._player.allow_video(command[1])

        elif command[0].upper() == "HELP":
            self._get_help()
        else:
            print(
                "Please enter a valid command, type HELP for a list of "
                "available commands.")

    def _get_help(self):
        """Displays all available commands to the user."""
        help_text = textwrap.dedent("""
        Available commands:
            NUMBER_OF_VIDEOS - Shows how many videos are in the library.
            SHOW_ALL_VIDEOS - Lists all videos from the library.
            PLAY <video_id> - Plays specified video.
            PLAY_RANDOM - Plays a random video from the library.
            STOP - Stop the current video.
            PAUSE - Pause the current video.
            CONTINUE - Resume the current paused video.
            SHOW_PLAYING - Displays the title, url and paused status of the video that is currently playing (or paused).
            CREATE_PLAYLIST <playlist_name> - Creates a new (empty) playlist with the provided name.
            ADD_TO_PLAYLIST <playlist_name> <video_id> - Adds the requested video to the playlist.
            REMOVE_FROM_PLAYLIST <playlist_name> <video_id> - Removes the specified video from the specified playlist
            CLEAR_PLAYLIST <playlist_name> - Removes all the videos from the playlist.
            DELETE_PLAYLIST <playlist_name> - Deletes the playlist.
            SHOW_PLAYLIST <playlist_name> - List all the videos in this playlist.
            SHOW_ALL_PLAYLISTS - Display all the available playlists.
            SEARCH_VIDEOS <search_term> - Display all the videos whose titles contain the search_term.
            SEARCH_VIDEOS_WITH_TAG <tag_name> -Display all videos whose tags contains the provided tag.
            FLAG_VIDEO <video_id> <flag_reason> - Mark a video as flagged.
            ALLOW_VIDEO <video_id> - Removes a flag from a video.
            HELP - Displays help.
            EXIT - Terminates the program execution.
        """)
        print(help_text)



"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

"""A video library class."""


from pathlib import Path
import csv


# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )

    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_video(self, video_id):
        """Returns the video object (title, url, tags) from the video library.
        Args:
            video_id: The video url.
        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)



"""A video player class."""




class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        self.id1= "Cats"
        self.id2="Home Tour"
        self.id3="Arts and Crafts"
        self.id4="Pranks"
        self.id5="Aircraft"
        print( self.id1, "ID=1\n", self.id2, "ID=2\n", self.id3 ,"ID=3 \n", self.id4, "ID4 \n" , self.id5, "ID=5")



    def play_video(self, video_id):
        """Plays the respective video.
        Args:

            video_id: The video_id to be played.
        """
        self.id1 = "Cats"
        self.id2 = "Home Tour"
        self.id3 = "Arts and Crafts"
        self.id4 = "Pranks"
        self.id5 = "Aircraft"
        if video_id== "1":
            print( self.id1 ,"Video is Playing")
        elif video_id== "2":
            print( self.id2 ,"Video is Playing")
        elif video_id == "3":
            print( self.id3, "Video is Playing")
        elif video_id == "4":
            print( self.id4, "Video is Playing")
        elif video_id == "5":
            print( self.id5, "Video is Playing")

    def stop_video(self):
        """Stops the current video."""

        print("Video Stopped")

    def play_random_video(self):
        """Plays a random video from the video library."""
        print ("Shuffle is On")

    def pause_video(self):
        """Pauses the current video."""

        print("Video Paused")

    def continue_video(self):
        """Resumes playing the current video."""

        print("Video Continued")

    def show_playing(self):
        """Displays video currently playing."""

        print("Current show")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        print("Playlist created", playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        print("add_to_playlist needs implementation")

    def show_all_playlists(self):
        """Display all playlists."""

        print("show_all_playlists needs implementation")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        if playlist_name == "1":
            print("Cats")
        elif playlist_name == "2":
            print("House Tours")
        elif playlist_name == "3":
            print("Arts and Crafts")
        elif playlist_name == "4":
            print("Pranks")
        elif playlist_name == "5":
            print("Aircraft")

        #print("Cats \n House Tours \n Arts and Crafts \n Pranks \n Aircraft")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.
        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.
        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.
        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.
        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")



"""A youtube terminal simulator."""


if __name__ == "__main__":
    print("""Hello and welcome to YouTube, what would you like to do?
    Enter HELP for list of available commands or EXIT to terminate.""")
    video_player = VideoPlayer()
    parser = CommandParser(video_player)
    while True:
        command = input("YT> ")
        if command.upper() == "EXIT":
            break
        try:
            parser.execute_command(command.split())
        except CommandException as e:
            print(e)
    print("YouTube has now terminated its execution. "
          "Thank you and goodbye!")



"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    #print ("Cat Video \nHouse Tour \nArts and Crafts \nPranks \nAircraft")
