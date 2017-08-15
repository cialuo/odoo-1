# -*- coding: utf-8 -*-
##############################################################################
#
#
#    Copyright (C) 2017 xiao (715294035@qq.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.
#
##############################################################################
import logging

_logger = logging.getLogger(__name__)

#线路基础数据
route_data = {
    #线路ID
    ('id', 'id'): None,
    #线路编码
    ('gprsId', 'gprsId'): None,
    #线路名称
    ('lineName', 'lineName'): None,
    #线路类型，无对应字段（1：单向环线；2：双向环线；3：双向线路）
    ('lineTypeId', None): None,
    #调车方式
    ('runTypeId', 'runTypeName'): {'single_shunt': 1, 'double_shunt':2},
    #调度类型
    ('dispatchModeId', 'schedule_type'): {'flexible_scheduling': 1003, 'planning_scheduling': 1004, 'hybrid_scheduling': 2027},
    #文档中提供的班制是 001,002,003 不符合文档中提供的类型long
    ('classSystemId', 'classSystemName'): {'one_shift': 1, 'two_shift': 2, 'three_shift': 3},
    #文档提供的类型是Long，只能提供 部门ID
    ('departmentId', 'department_id'): None,
    #是否环线，无对应字段（0：环线；1：非环线）
    ('isRoundLine', None): None,
    #是否夜班线路，无对应字段（0：非夜班；1：夜班线路）
    ('isNight', None): None,
    #是否跨天，无对应字段(0：跨天；1：非跨天)
    ('isCrossDay', None): None,
    #票价，无对应字段
    ('ticketPrice', None): None,
    #线路开通日期，无对应字段
    ('startDate', None): None,
    #线路停运日期，无对应字段
    ('endDate', None): None,
    #是否人工售票，无对应字段（0：非人工；1：人工售票）
    ('isArtificialTicket', None): None,
    #是否显示线路辅助点，无对应字段（0：不显示；1：显示）
    ('isShowPoint', None): None,
    #是否显示站点名，无对应字段（0：不显示；1：显示）
    ('isShowStationName', None): None,
    #以下三个字段文档未描述
    # 'lineStart': '',
    # 'lineEnd': '',
    # 'companyId': '',
}

#站点基础数据
station_data = {}

#车辆基础数据
fleet_data = {}

#人员基础数据
employee_data = {}

#线路计划基础数据
scheduleplan_data = {}

#调度线路基础数据
#无对应的数据库表

#调度参数基础数据
config_data = {}

origin_data = {
    'route_manage.route_manage': route_data,
    'opertation_resources_station': station_data,
    'fleet.vehicle': fleet_data,
    'hr.employee': employee_data,
    'scheduleplan.excutetable': scheduleplan_data,
    'dispatch.config.settings': config_data,
}

def dict_transfer(table, data):
    """
    
    :param table: 表名
    :param data: 同步数据
    :return: 
    """
    if origin_data.get(table):
        table_data = origin_data[table]
        new_data = {}
        if isinstance(data, dict):
            for key in data.keys():
                for k, v in table_data.iteritems():
                    if not k[1]:
                        continue
                    if key == k[1]:
                        if v:
                            value = v[data[key]]
                        else:
                            value = data[key]
                        new_data.update({k[0]: value})
            _logger.info('origin Data: %s', data)
            _logger.info('Prepare New Data: %s', new_data)
            return new_data