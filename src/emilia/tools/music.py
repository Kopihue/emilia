from emilia.lib.audio import AudioFile

from kopitools import log
import pyaudio

from typing import Callable
from pathlib import Path
from threading import Thread

class Music:
    def __init__(self, client: pyaudio.PyAudio):
        self.client = client
        self.music_dir = Path().home().joinpath("Music")
        self.active_threads: dict[str, Thread] = {}

        if not self.music_dir.exists():
            raise FileNotFoundError("$HOME/Music/ does not exist")

    def _generate_thread(self, target: Callable, *args, **kwargs) -> Thread:
        return Thread(
            target=target,
            args=args,
            kwargs=kwargs
        )

    def get_songs(self) -> str:
        """
        Use this tool to get all of the songs in the system

        Args:
            None

        Returns:
            str: Containing every song
        """
        log("Obtaining songs!").info()
        return "\n".join(song.name for song in self.music_dir.iterdir())

    def play_song(self, song: str) -> str:
        """
        Use this tool to play a song

        Args:
            str: name of the song plus the suffix

        Returns:
            str: Message containing if the song was succesfully played

        """
        instance = AudioFile(
            self.client,
            self.music_dir.joinpath(song),
            self._song_naturally_finished,
        )

        if found := self.active.get(song):
            found.close()

        self.active[song] = instance

        try:
            log(f"Playing song: {song}!").success()
            instance.play()
        except Exception as e:
            return f"ERROR: {e}"
        else:
            return f"{song} is succesfully playing!"

    def play_song_on_repeat(self, song: str) -> str:
        """
        Use this tool to play the given song on repeat

        Args:
            str: name of the song plus the suffix

        Returns:
            None
        """
        while True:
        return f"Playing {song} on repeat!"

    def pause_song(self, song: str) -> str:
        """
        Use this tool to pause the given song

        Args:
            str: name of the song plus the suffix

        Returns:
            str: Message containing if the song was succesfully paused
        """
        if instance := self.active.get(song):
            log(f"Pausing song: {song}!").success()
            instance.pause()
            return f"{song} succesfully paused!"
        else:
            return f"{song} is not actively playing!"

    def resume_song(self, song: str):
        """
        Use this tool to resume the given song

        Args:
            str: name of the song plus the suffix

        Returns:
            str: Message containing if the song was succesfully resumed
        """
        if instance := self.active.get(song):
            log(f"Resuming song: {song}!").success()
            instance.resume()
            return f"{song} succesfully resumed!"
        else:
            return f"{song} is not actively playing!"

    def close_song(self, song: str):
        """
        Use this tool to resume the given song

        Args:
            str: name of the song plus the suffix

        Returns:
            str: Message containing if the song was succesfully closed
        """
        if instance := self.active.get(song):
            log(f"Closing song: {song}!").success()
            instance.close()
            self.active.pop(song, None)
            return f"{song} succesfully closed!"
        else:
            return f"{song} is not actively playing!"

    def close_all_songs(self):
        """
        Use this tool to close every song

        Args:
            None

        Returns:
            None
        """
        for song, current in list(self.active.items()):
            log(f"Closing song: {song}!").success()
            current.close()
            self.active.pop(song, None)

    # callback to AudioFile
    def _song_naturally_finished(self, instance: AudioFile):
        for song, current in self.active.items():
            if current is instance:
                self.active.pop(song, None)
                break
