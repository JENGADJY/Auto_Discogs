import schedule
import time
from .exec import auto_exe


def exc_data():
  auto_exe()


  schedule.every(1).minutes.do(exc_data)

  while True:
    schedule.run_pending()
    time.sleep(1)
    exc_data()
