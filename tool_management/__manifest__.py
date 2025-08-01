# tool_management/__manifest__.py

{
    'name': 'Tool Management System',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Manage tool requests, allocations, and returns',
    'depends': ['base', 'hr', 'project','hr_recruitment'],
    'data': [
        'security/tool_security.xml',
        'security/ir.model.access.csv',
        'views/menus.xml', 
        'views/request_views.xml',
        'views/tool_views.xml',  
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}