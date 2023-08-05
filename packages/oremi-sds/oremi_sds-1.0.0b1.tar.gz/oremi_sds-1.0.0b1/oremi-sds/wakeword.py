# Copyright 2023 Sébastien Demanou. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
import tempfile
from typing import Callable, Coroutine

from pocketsphinx import Config, Decoder

from .models import DetectedSound, DictionaryEntry, WakewordSetting
from .trace import Trace
from .vars import APP_ID, ENCODING

__all__ = [
  'WakewordSetting',
  'WakewordEngine',
]


class WakewordEngine:
  """Class for performing wake word detection."""

  def __init__(
    self,
    *,
    setting: WakewordSetting,
    on_sound_detect: Callable[[DetectedSound], Coroutine],
    logger: Trace,
  ):
    self._logger = logger
    self._setting = setting
    self._on_sound_detect = on_sound_detect
    config = Config(
      lm = None,
      hmm = setting.model,
      dict = setting.dictionary,
      kws_threshold = 1e-10,
    )

    self._decoder = Decoder(config)
    self._configure_keyphrases()

  def _configure_keyphrases(self):
    """Configures the keyphrases for the wake word detection."""
    temp_dir = tempfile.mkdtemp()
    filename = os.path.join(temp_dir, 'keyphrases.list')

    self._logger.info(f'Creating keyphrases file {filename}')
    with open(filename, 'w', encoding = ENCODING) as file:
      for entry in self._setting.wakewords + self._setting.discriminants:
        file.write(f'{entry.word}\n')
        self._add_dictionary_entry(entry)

    self._decoder.add_kws(APP_ID, filename)
    self._decoder.activate_search(APP_ID)

  def _add_dictionary_entry(self, entry: DictionaryEntry) -> None:
    """
    Adds a new entry to the wake word dictionary.

    Args:
      entry (DictionaryEntry): The entry to add to the dictionary.
    """
    for index, phone in enumerate(entry.phones):
      self._logger.info(f'Adding new word "{entry.word}" to the dictionary')

      word = entry.word if index == 0 else f'{entry.word}({index + 1})'

      try:
        self._decoder.add_word(word, phone)
      except RuntimeError as error:
        self._logger.error(error)

  def is_discriminant(self, word: str) -> bool:
    """
    Checks whether a given word is a discriminant.

    Args:
        word (str): The word to check.

    Returns:
        bool: True if the word is a discriminant, otherwise False.
    """
    return any(item for item in self._setting.discriminants if item.word == word)

  def start_utt(self) -> None:
    """Starts a new utterance for the wake word detection."""
    self._decoder.start_utt()

  def end_utt(self) -> None:
    """Ends the current utterance for the wake word detection."""
    self._decoder.end_utt()

  async def process_raw(self, chunk: bytes) -> float:
    self._decoder.process_raw(chunk, False, False)

    hypothesis = self._decoder.hyp()

    if hypothesis is None:
      return False

    is_discriminant = self.is_discriminant(hypothesis.hypstr)

    self._decoder.end_utt()
    self._decoder.start_utt()

    if is_discriminant:
      self._logger.warning(f'Discriminant wakeword detected: {hypothesis.hypstr}, score {hypothesis.score:.2f}')
      return False

    await self._on_sound_detect('wakeword', hypothesis.score)
    return True
