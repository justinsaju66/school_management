# -*- coding: utf-8 -*-
{
    'name': "School",
    'version': '1.0',
    'depends': ['base','hr','sale', 'web','website'],
    'author': "Author Name",
    'category': 'all',
    'sequence':1,
    'description': """
    School Management
    """,
    'data': [
         'security/school_management_group.xml',
         'security/school_management_record_rules.xml',
         'security/ir.model.access.csv',
         'data/automation.xml',
         'data/ir_sequence_data.xml',
         'data/manage_department_data.xml',
         'data/manage_subject_data.xml',
         'data/manage_class_data.xml',
         'data/manage_event_email_data.xml',
         'data/ir_cron_data.xml',
         'data/registration_templates.xml',
         'data/leave_template.xml',
         'data/event_template.xml',
         'views/school_management_event_snippet.xml',
         'views/student_registration_views.xml',
         'views/academic_year_views.xml',
         'views/manage_class_views.xml',
         'views/manage_subject_views.xml',
         'views/manage_department_views.xml',
         'views/manage_club_views.xml',
         'views/manage_event_view.xml',
         'views/sale_order_views.xml',
         'views/res_partner_views.xml',
         'views/manage_leave_views.xml',
         'views/manage_exam_views.xml',
         'views/registration_website_view.xml',
         'views/leave_website_view.xml',
         'views/event_website_view.xml',
         'views/event_snippet_view.xml',
         'report/ir.actions.report.xml',
         'report/student_leave_report_template.xml',
         'report/student_information_template.xml',
         'wizard/leave_information.xml',
         'wizard/student_information.xml',
        'views/website_menu.xml',
        'views/school_management_menu.xml',

    ],
    "assets": {

        'web.assets_backend': [

            'school_management/static/src/js/action_manager.js',

        ],
        'web.assets_frontend': ['school_management/static/src/xml/dynamic_courosel.xml',
                                'school_management/static/src/js/snippet.js',
                                ],

    },

    'application': True,
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
