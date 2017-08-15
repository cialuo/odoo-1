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

#线路基础数据
route_data = {}

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

origin_data = {
    'route_manage.route_manage': route_data,
    'opertation_resources_station': station_data,
    'fleet.vehicle': fleet_data,
    'hr.employee': employee_data,
    'scheduleplan.excutetable': scheduleplan_data,
    ''

}