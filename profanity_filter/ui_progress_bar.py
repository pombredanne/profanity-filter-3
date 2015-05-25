"""
Progress bar encapsulation
"""

# Copyright (c) Timur Iskhakov.
# Distributed under the terms of the MIT License.


import progressbar


class UIProgressBar:
    __widgets = [' ', progressbar.Percentage(), ' ', progressbar.Bar(), ' ', progressbar.ETA()]

    def __init__(self, message, max_value):
        """
        :param message: :class:`str` Message to print
        :param max_value: :class:`int`, Number of steps for bar
        """

        self.progress_bar = progressbar.ProgressBar(widgets=[message] + UIProgressBar.__widgets,
                                                    maxval=max_value)
        self.value = 0

    def start(self):
        self.progress_bar.start()

    def step(self):
        self.value += 1
        self.progress_bar.update(self.value)

    def finish(self):
        self.progress_bar.finish()
