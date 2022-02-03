from typing import Collection

class ZoneController:
  def buildZoneId(zonesCollection: Collection):
    zoneId = 0
    zonesAmount = zonesCollection.count_documents({})

    if zonesAmount > 0:
      descending = -1
      lastZone = zonesCollection.find().sort('_id', descending).limit(1)

      for lastZoneData in lastZone:
        zoneId = lastZoneData['_id'] + 1

    return zoneId
