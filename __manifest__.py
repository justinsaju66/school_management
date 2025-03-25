# -*- coding: utf-8 -*-

{
    'name': "School",
    'version': '1.0',
    'depends': ['base','hr','sale'],
    'author': "Author Name",
    'category': 'all',
    'sequence':1,
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
         'security/ir.model.access.csv',
         'security/school_management_group.xml',
         'data/automation.xml',
         'data/ir_sequence_data.xml',
         'data/manage_department_data.xml',
         'data/manage_subject_data.xml',
         'data/manage_class_data.xml',
         'data/manage_event_email_data.xml',
         'data/ir_cron_data.xml',
         'views/student_registration_views.xml',
         'views/academic_year_views.xml',
         'views/manage_class_views.xml',
         'views/manage_subject_views.xml',
         'views/manage_department_views.xml',
         'views/school_management_menu_views.xml',
         'views/manage_club_views.xml',
         'views/manage_event_view.xml',
         'views/sale_order_views.xml',
         'views/res_partner_views.xml',
         'views/manage_leave_views.xml',
         'views/manage_exam_views.xml',

    ],
    # data files containing optionally loaded demonstration data
    #    'demo': [
    #     'data/manage_department_demo.xml',
    #      'data/manage_subject_demo.xml',
    #      'data/manage_class_demo.xml',
    #     ],
    'application': True,
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}