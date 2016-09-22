#!/bin/evn/python
# encoding:utf8
import MySQLdb
import time


server = "127.0.0.1"
username = "mozbx"
password = "fLHrZHm8g5LvDWh6KGty"
dbname = "zabbix"
port = 3306


def main():
    # result = get_values()
    result = get_uptime()
    print result
    return result


def get_warnning():
    sql = "select  h.host, t.lastchange, t.description, t.priority from \
        triggers t join functions f on t.triggerid = f.triggerid \
        join items i on f.itemid = i.itemid \
        join hosts h on h.hostid = i.hostid where t.value = 1"
    result = select_mysql(sql)
    return result


def get_status():
    sql = "select hostid,status,host,available from hosts"
    sql_result = select_mysql(sql)
    host_dic = {"templates": 0, "host": 0, "disable": 0, "proxy": 0}
    for i in sql_result:
        if i[1] == 5:
            host_dic["proxy"] = host_dic["proxy"] + 1
            host_dic["host"] = host_dic["host"] + 1
        elif i[1] == 3:
            host_dic["templates"] = host_dic["templates"] + 1
        elif i[1] == 1:
            host_dic["disable"] = host_dic["disable"] + 1
        elif i[1] == 0:
            host_dic["host"] = host_dic["host"] + 1
    return host_dic


def get_uptime():
    end_time = int(time.time()) - 300
    sql = 'select ho.hostid, max(h.clock), h.value from history_uint h \
        join items i on i.itemid = h.itemid \
        join hosts ho on ho.hostid = i.hostid \
        where h.clock > ' + str(end_time) + ' \
        and i.key_ = "system.uptime" group by h.itemid '
    sql_result = select_mysql(sql)
    return sql_result


def get_mem_total():
    end_time = int(time.time()) - 86400
    sql = 'select i.hostid, h.value, ho.host from \
        items i join history_uint h on i.itemid = h.itemid \
        join hosts ho on i.hostid = ho.hostid \
        where i.key_ like "vm.memory.size[total]" \
        and  h.clock > ' + str(end_time) + ' group by (ho.host)'
    sql_result = select_mysql(sql)
    return sql_result


def get_mem_free():
    end_time = int(time.time()) - 300
    sql = 'select i.hostid, h.clock, h.value from \
        items i join history_uint h on i.itemid = h.itemid \
        join hosts ho on i.hostid = ho.hostid \
        where i.key_ like "vm.memory.size[free]" \
        and h.clock > ' + str(end_time) + ' group by (ho.host)'
    sql_result = select_mysql(sql)
    return sql_result


def get_cpu_idle():
    end_time = int(time.time()) - 300
    sql = 'select i.hostid, t.clock, t.value_min, t.value_max, t.value_avg from \
        items i join trends t on i.itemid = t.itemid \
        join hosts ho on i.hostid = ho.hostid \
        where i.key_ like "system.cpu.util[,idle]" \
        and t.clock > ' + str(end_time) + ' group by (ho.host)'
    sql_result = select_mysql(sql)
    return sql_result


def get_cpu_iowait():
    end_time = int(time.time()) - 300
    sql = 'select i.hostid, t.clock, t.value_min, t.value_max, t.value_avg from \
        items i join trends t on i.itemid = t.itemid \
        join hosts ho on i.hostid = ho.hostid \
        where i.key_ like "system.cpu.util[,iowait]" \
        and t.clock > ' + str(end_time) + ' group by (ho.host)'
    sql_result = select_mysql(sql)
    return sql_result


def get_cpu_load():
    end_time = int(time.time()) - 300
    sql = 'select i.hostid, t.clock, t.value_min, t.value_max, t.value_avg from \
        items i join trends t on i.itemid = t.itemid \
        join hosts ho on i.hostid = ho.hostid \
        where i.key_ like "system.cpu.load[percpu,avg5]" \
        and t.clock > ' + str(end_time) + ' group by (ho.host)'
    sql_result = select_mysql(sql)
    return sql_result


def get_net_in():
    end_time = int(time.time()) - 300
    sql = 'select i.key_, i.hostid, t.clock, t.value_min, t.value_max, t.value_avg from \
        items i join trends_uint t on i.itemid = t.itemid \
        join hosts ho on i.hostid = ho.hostid \
        where i.key_ like "net.if.in%" \
        and t.clock > ' + str(end_time) + ' group by (ho.host)'
    sql_result = select_mysql(sql)
    return sql_result


def get_net_out():
    end_time = int(time.time()) - 300
    sql = 'select i.key_, i.hostid, t.clock, t.value_min, t.value_max, t.value_avg from \
        items i join trends_uint t on i.itemid = t.itemid \
        join hosts ho on i.hostid = ho.hostid \
        where i.key_ like "net.if.out%" \
        and t.clock > ' + str(end_time) + ' group by (ho.host)'
    sql_result = select_mysql(sql)
    return sql_result


def select_mysql(sql):
    try:
        conn = MySQLdb.connect(host=server,
                               user=username,
                               passwd=password,
                               db=dbname,
                               port=port,
                               charset='utf8'
                               )
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__ == '__main__':
    main()
