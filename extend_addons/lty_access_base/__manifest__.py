# -*- coding: utf-8 -*-
{
    'name': "lty_access_base",

    'summary': """
        与调度的数据接口""",

    'description': """
        离线计算:
            1）路线分时客流
            2）站点分时客流
            3）准点与滞站
            4）乘客满意度
            5）服务保障能力
            6）车辆到站预测准点
            7）行车规则
            8）配车方案
            
        实时计算:
            1）实时线路信息
            2）实时车辆信息
            3）实时站点信息
            4）线路时段意外高峰
            5）线路时段意外低峰
            6）站点意外高峰
            7）站点意外低峰
    """,

    'author': "He",
    'website': "http://www.lantaiyuan.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['scheduling_parameters'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/lineTimeTopic_view.xml',
        'views/stationTimeTopic_view.xml',
        'views/punctuality_detention_topic_view.xml',
        'views/menus.xml'
    ],
}