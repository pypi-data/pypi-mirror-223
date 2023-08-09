import os
import datetime
from time import sleep

from colr import color
from pygame import mixer

from pymodoro import Pymodoro
from settings import CLEAR_CMD

mixer.init()
mixer.music.load("./assets/sound.mp3")


class PymodoroCli(Pymodoro):
    def __init__(
        self,
        pomodoros: int = 1,
        pomodoro_time: int = 25,
        short_break_time: int = 5,
        long_break_time: int = 15,
    ) -> None:
        super().__init__(
            pomodoros, pomodoro_time, short_break_time, long_break_time
        )

    @staticmethod
    def wait() -> None:
        input("press any key when you ready")

    def start_pomodoro(self) -> None:
        os.system(CLEAR_CMD)
        print(
            color(" Pomodoro ", back="red", style="bold"),
            f"{self.pomodoros_done} / {self.pomodoros}",
        )

        super().start_pomodoro()

        mixer.music.play()
        self.wait()
        mixer.music.stop()

    def start_short_break(self) -> None:
        os.system(CLEAR_CMD)
        print(color(" Short Break ", back="cyan", style="bold"))

        super().start_short_break()

        mixer.music.play()
        self.wait()
        mixer.music.stop()

    def start_long_break(self) -> None:
        os.system(CLEAR_CMD)
        print(color(" Long Break ", back="blue", style="bold"))

        super().start_long_break()

        mixer.music.play()
        self.wait()
        mixer.music.stop()

    def run(self) -> None:
        os.system(CLEAR_CMD)

        minutes = (
            int(input("How many hours do you plan to work, sir?\n\n")) * 60
        )
        self.pomodoros = (
            minutes // 25 if not minutes % 25 else minutes // 25 + 1
        )

        os.system(CLEAR_CMD)

        total_long_breaks = (self.pomodoros - 1) // 4
        total_long_breaks_time = total_long_breaks * self.long_break_time

        total_short_breaks = max(0, self.pomodoros - total_long_breaks - 1)
        total_short_breaks_time = total_short_breaks * self.short_break_time

        total_work_time = self.pomodoros * self.pomodoro_time

        ends_at = datetime.datetime.now() + datetime.timedelta(
            0,
            (
                total_short_breaks_time
                + total_long_breaks_time
                + total_work_time
            )
            * 60,
        )

        print(
            color(
                f" It ends at {ends_at.hour}:{ends_at.minute} ",
                back="green",
                style="bold",
            )
        )

        sleep(10)

        super().run()

        print(color(" Congratulations Sir! ", back="green", style="bold"))
