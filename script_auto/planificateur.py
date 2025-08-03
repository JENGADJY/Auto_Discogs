import schedule
import time
from . import exec


def exc_data():
  exec.auto_exe()


  schedule.every(1).minutes.do(exc_data)

  while True:
    schedule.run_pending()
    time.sleep(1)
    exc_data()
