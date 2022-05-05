required_params = {
  'user': {
    'create': ['name', 'email', 'password'],
    'read': ['email', 'password']
  },
  'irrigation_zone': {
    'create': ['name', 'description', 'size', 'user_id']
  },
  'culture': {
    'create': ['irrigation_zone_id', 'name', 'type', 'planting_date', 'coefficient_et', 'phase', 'geographic_coordinates']
  }
}
