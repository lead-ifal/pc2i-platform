from worker import worker
import time
from datetime import datetime
from typing import Collection
from app.controllers.zone_controller import ZoneController
from app.extensions import database

scheduled_irrigations: Collection = database.db.scheduled_irrigations



class ScheduleIrrigationService:
  #@worker
  def verify_schedule():
    looping = True
    hour_to_seconds = 3600
    minutes_to_seconds = 60
    shorter_time = 86400
    while looping == True:
      current_time = datetime.now().time()
      current_time = current_time.second + current_time.minute * minutes_to_seconds + current_time.hour * hour_to_seconds
      day = datetime.today().weekday()
      schedule_list = scheduled_irrigations.find({})
      for schedule in schedule_list:
        if day in schedule["days"]:
          if schedule["moment_of_activation"] < shorter_time and schedule["moment_of_activation"] > current_time:
            shorter_time = schedule["moment_of_activation"]
      wait = shorter_time - current_time
      next_irrigation = scheduled_irrigations.find_one({'moment_of_activation': shorter_time})
      time.sleep(wait)
      ZoneController.toggle_irrigation(next_irrigation["irrigation_zone_id"])
