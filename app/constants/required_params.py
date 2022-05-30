required_params = {
  'users': {
    'create': ['name', 'email', 'password'],
    'read': ['email', 'password']
  },
  'irrigation_zones': {
    'create': ['name', 'description', 'size', 'user_id']
  },
  'cultures': {
    'create': ['irrigation_zone_id', 'name', 'type', 'planting_date', 'coefficient_et', 'phase', 'geographic_coordinates']
  }
}
