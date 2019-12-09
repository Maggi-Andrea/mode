import mode


class MyService(mode.LoggingMixin, mode.Service):
  
    def __init__(self, *args,
                 override_logging:bool=False,
                 **kwargs)->None:
      super().__init__(*args,
                 override_logging=override_logging,
                 **kwargs)
  
    async def on_first_start(self) -> None:
        self.setup_logging()
        
    async def on_start(self):
        self.setup_redirect_stdouts()

    async def on_started(self) -> None:
        self.log.info('Service started.')
        
    @mode.Service.task
    async def _background_task(self) -> None:
        print('BACKGROUND TASK STARTING')
        while not self.should_stop:
            await self.sleep(1.0)
            print('BACKGROUND SERVICE WAKING UP')

def new_worker():
  return mode.Worker(
      MyService(loglevel='INFO',),
      loglevel='INFO',
      logfile=None,  # stderr
      # when daemon the worker must be explicitly stopped to end.
      daemon=True,
  )


if __name__ == '__main__':
  new_worker().execute_from_commandline()
    
