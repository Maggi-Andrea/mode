'''
Created on 15 nov 2019

@author: Andrea Maggi
'''

import logging as _logging
import sys
from logging import Logger, StreamHandler
from typing import (
  Any, #@UnusedImport
  Dict,
  IO,
  List,
  Optional,
  Union,
)

from .utils import logging


class LoggingMixin:
  
  stdout: IO
  stderr: IO
  quiet: bool
  logging_config: Optional[Dict]
  loglevel: Optional[Union[str, int]]
  logfile: Optional[Union[str, IO]]
  loghandlers: List[StreamHandler]
  redirect_stdouts: bool
  redirect_stdouts_level: int

  def __init__(
        self, *args, 
        quiet: bool = False,
        logging_config: Dict = None,
        loglevel: Union[str, int] = None,
        logfile: Union[str, IO] = None,
        redirect_stdouts: bool = True,
        redirect_stdouts_level: logging.Severity = None,
        stdout: IO = sys.stdout,
        stderr: IO = sys.stderr,
        loghandlers: List[StreamHandler] = None,
        override_logging: bool = True,
        **kwargs: Any) -> None:
    self.quiet = quiet
    self.logging_config = logging_config
    self.loglevel = loglevel
    self.logfile = logfile
    self.loghandlers = loghandlers or []
    self.redirect_stdouts = redirect_stdouts
    self.redirect_stdouts_level = logging.level_number(
      redirect_stdouts_level or 'WARN')
    self.override_logging = override_logging
    if stdout is None:
      stdout = sys.stdout
    self.stdout = stdout
    if stderr is None:
      stderr = sys.stderr
    self.stderr = stderr
    super().__init__(*args, **kwargs)
              
  def say(self, msg: str) -> None:
    """Write message to standard out."""
    self._say(msg)

  def carp(self, msg: str) -> None:
    """Write warning to standard err."""
    self._say(msg, file=self.stderr)

  def _say(self,
           msg: str,
           file: Optional[IO] = None,
           end: str = '\n',
           **kwargs: Any) -> None:
    if file is None:
      file = self.stdout
    if not self.quiet:
      print(msg, file=file, end=end, **kwargs)  # noqa: T003
              
  def setup_logging(self) -> None:
    if self.override_logging:
      self._setup_logging()
  
  def _setup_logging(self) -> None:
    _loglevel: int = 0
    try:
      _loglevel = logging.setup_logging(
        loglevel=self.loglevel,
        logfile=self.logfile,
        logging_config=self.logging_config,
        loghandlers=self.loghandlers,
      )
    except Exception as exc:
      try:
        self.stderr.write(f'CANNOT SETUP LOGGING: {exc!r} from ')
        import traceback
        traceback.print_stack(file=self.stderr)
      except Exception:
        pass
      raise
    self.on_setup_root_logger(_logging.root, _loglevel)
            
  def setup_redirect_stdouts(self) -> None:
    if self.override_logging and self.redirect_stdouts:
      self._redirect_stdouts()
            
  def _redirect_stdouts(self) -> None:
    self.add_context(
      logging.redirect_stdouts(severity=self.redirect_stdouts_level))
            
  def on_setup_root_logger(self,
                           logger: Logger,
                           level: int) -> None:
    ...