required_params = {
  'users': {
    'create': ['name', 'email', 'password'],
    'read': ['email', 'password']
  },
  'irrigation_zones': {
    'create': ['user_id', 'name', 'description', 'size', 'irrigation_type'],
    'schedule': ['irrigation_zone_id', 'liters_of_water', 'time', 'day']
  },
  'cultures': {
    'create': ['irrigation_zone_id', 'name', 'type', 'planting_date', 'phase', 'geographic_coordinates']
  },
  'sensors': {
    'create': ['culture_id', 'name'],
    'read': ['culture_id']
  },

}
