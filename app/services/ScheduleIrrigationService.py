from worker import worker
import time
import schedule
from datetime import datetime,timedelta
from typing import Collection
from app.controllers.zone_controller import ZoneController
from app.extensions import database

scheduled_irrigations: Collection = database.db.scheduled_irrigations



class ScheduleIrrigationService:
  @worker
  def active_schedule(irrigation_zone_id):
    ZoneController.toggle_irrigation(irrigation_zone_id)
    return schedule.CancelJob

  def verify_schedule():
    day = datetime.today().weekday()
    schedule_list = scheduled_irrigations.find({})
    for irrigation_scheduled in schedule_list:
      if day in irrigation_scheduled["days"]:
        activation_moment = datetime.strptime(irrigation_scheduled["time"], '%H:%M:%S').time()
        duration = datetime.strptime(irrigation_scheduled["duration"], '%H:%M:%S').time()
        stop_moment = timedelta(hours=activation_moment.hour, minutes=activation_moment.minute,  seconds=activation_moment.second )+ timedelta(hours=duration.hour,minutes=duration.minute,
        seconds=duration.second)
        schedule.every().day.at(str(activation_moment)).do(ScheduleIrrigationService.active_schedule,irrigation_zone_id=irrigation_scheduled["irrigation_zone_id"])
        schedule.every().day.at(str(stop_moment)).do(ScheduleIrrigationService.active_schedule,irrigation_zone_id=irrigation_scheduled["irrigation_zone_id"])
  @worker
  def worker_schedule():
    schedule.every().day.at("00:00").do(ScheduleIrrigationService.verify_schedule)
    while True:
      schedule.run_pending()
      time.sleep(1)


