required_params = {
  'users': {
    'create': ['name', 'email', 'password'],
    'read': ['email', 'password']
  },
  'irrigation_zones': {
    'create': ['user_id', 'name', 'description', 'size', 'irrigation_type'],
    'schedule': ['irrigation_zone_id', 'liters_of_water', 'time', 'days','moment_of_activation'],
    'delete': ['irrigation_zone_id'],
    'delete_schedule': ['schedule_id'],
    'update': ['irrigation_zone_id', 'user_id', 'name', 'description', 'size', 'irrigation_type'],
    'update_schedule': ['schedule_id', 'irrigation_zone_id', 'liters_of_water', 'time', 'days','moment_of_activation']
  },
  'cultures': {
    'create': ['irrigation_zone_id', 'name', 'type', 'planting_date', 'phase', 'geographic_coordinates'],
    'delete': ['culture_id'],
    'update': ['culture_id', 'irrigation_zone_id', 'name', 'type', 'planting_date', 'phase', 'geographic_coordinates']
  },
  'sensors': {
    'create': ['culture_id', 'name'],
    'read': ['culture_id']
  },

}
