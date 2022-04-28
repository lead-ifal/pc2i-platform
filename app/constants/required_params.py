required_params = {
  'user': {
    'create': ['name', 'email', 'password'],
    'read': ['email', 'password']
  },
  'zone': {
    'create': ['name', 'description', 'size']
  },
  'culture': {
    'create': ['zone_id', 'name', 'type', 'planting_date', 'coefficient_et', 'phase', 'geographic_coordinates']
  }
}
