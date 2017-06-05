# -*- coding: utf-8 -*-
{
    'name': "员工成长管理",

    'summary': """
        内部培训：
            培训计划，培训课程，培训考试，培训签到，培训成绩管理，培训师管理
        内部培训：
            外部培训计划，外部培训课程
    """,

    'description': """
    """,
    'author': "He",
    'website': "http://www.lantaiyuan.com/",
    'category': 'Optional Edition',
    'version': '0.1',
    'depends': ['base','employees'],
    'data': [
        'security/security_data.xml',
        # 'security/ir.model.access.csv',
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
        'views/menus.xml',
    ],
    #'qweb': ['static/src/xml/examination.xml'],
    'application': True
}