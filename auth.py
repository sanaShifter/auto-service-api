PERMISSIONS = {
    'Менеджер': [
        'view_requests', 'create_requests', 'edit_requests', 'delete_requests',
        'assign_mechanic', 'change_status', 'add_comments', 'view_statistics',
        'manage_users', 'manage_parts'
    ],
    'Автомеханик': [
        'view_requests', 'change_status', 'add_comments', 'manage_parts'
    ],
    'Оператор': [
        'view_requests', 'create_requests', 'edit_requests'
    ],
    'Заказчик': [
        'view_requests'
    ],
    'Менеджер по качеству': [
        'view_requests', 'view_statistics', 'extend_deadline', 'view_quality_reports'
    ]
}

def has_permission(user_type, permission):
    return permission in PERMISSIONS.get(user_type, [])