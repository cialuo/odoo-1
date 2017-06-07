# -*- coding: utf-8 -*-
{
    'name': "员工成长管理",

    'summary': """
        员工成长管理
    """,

    'description': """
    """,
    'author': "He",
    'website': "http://www.lantaiyuan.com/",
    'category': 'Optional Edition',
    'version': '0.1',
    'depends': ['base','employees','security_manage_menu','vehicle_manage_menu'],
    'data': [
        'security/security_data.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/course_typ_view.xml',
        'views/training_teacher_view.xml',
        'views/questions_view.xml',
        'views/test_paper_view.xml',
        'views/course_view.xml',
        'views/curriculum_schedule_view.xml',
        'views/pendingAudit_return_view.xml',
        'views/training_plan_view.xml',
        'views/punch_recording.xml',
        'views/examination_view.xml',
        'views/external_plan_return_view.xml',
        'views/external_training_plan_view.xml',
        'views/external_curriculum_schedule_view.xml',
        'views/safety_training_page.xml',
        'views/menus.xml',
    ],
    #'qweb': ['static/src/xml/examination.xml'],
    'application': True
}