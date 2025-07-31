# tool_management/__manifest__.py

{
    'name': 'Tool Management System',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Manage tool requests, allocations, and returns',
    'depends': ['base', 'hr', 'project'],
    'data': [
        'security/tool_security.xml',
        'security/ir.model.access.csv',
        'views/tool_views.xml',
         'views/request_views.xml',
        
       
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}