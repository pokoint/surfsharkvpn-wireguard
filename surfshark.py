import os
import sqlite3


def manage_surfshark_node():
    sql3 = sqlite3.connect("node.db")
    while True:
        os.system('clear')
        print("已添加节点：")
        try:
            server_list = sql3.execute('select * from node')
            for item in server_list:
                print(f'id：{item[0]} 名称：{item[1]} 地址：{item[2]} 端口：{item[3]} 公钥：{item[4]}')
        except sqlite3.OperationalError:
            sql3.execute(
                'create table node (id integer primary key, node_name varchar(16), node_host varchar(50), node_port varchar(6), node_key varchar(50) )')
            sql3.commit()
        print('1、添加 surfshark 节点')
        print('2、删除 surfshark 节点')
        print('Q、返回主菜单')
        choose = input("请选择：")
        if choose == '1':
            while True:
                #os.system('clear')
                name = input("自定义名称：")
                host = input("节点地址（IP）：")
                port = input("节点端口：")
                s_key = input("节点公钥：")
                print(f'名称：{name} 地址：{host} 端口：{str(port)} 公钥：{s_key}')
                choose_1 = input('确认输入无误？ (y/n/q)：')
                if choose_1 == 'y' or choose_1 == 'Y':
                    sql3.execute('insert into node (node_name, node_host, node_port, node_key ) values (?,?,?,?)',(name,host,port,s_key))
                    sql3.commit()
                    choose_2 = input('是否继续添加(y/n)：')
                    if choose_2 != 'y':
                        break
                    else:
                        pass
                elif choose == 'q' or choose == 'Q':
                    break
                else:
                    pass
        elif choose == '2':
            node_id = input("要删除的节点id：")
            choose_1 = input("确定删除？(y/n)")
            if choose_1 == 'y':
                sql3.execute('delete from student where id = ?', node_id)
                sql3.commit()
                print("删除成功！")
                os.system('pause')
            else:
                a = input("删除取消！回车继续")
        else:
            break


def use_surfshark_out():
    sql3 = sqlite3.connect("node.db")
    while True:
        os.system('clear')
        print("已添加节点：")
        try:
            server_list = sql3.execute('select * from node')
            for item in server_list:
                print(f'id：{item[0]} 名称：{item[1]} 地址：{item[2]} 端口：{item[3]} 公钥：{item[4]}')
        except sqlite3.OperationalError:
            sql3.execute(
                'create table node (id integer primary key, node_name varchar(16), node_host varchar(50), node_port varchar(6), node_key varchar(50) )')
        node_id = ''
        while node_id == '':
            node_id = input("请选择出站节点：")
        loc_ipv4 = input("输入本地IPv4，回车自动检测(nat机请自己输入内网IP)：")
        while loc_ipv4 == '':
            os.system('systemctl stop wg-quick@wg')
            os.system('echo "nameserver 8.8.8.8 \n nameserver 8.8.4.4" >> /etc/resolv.conf')
            os.system('service networking restart')
            res = os.popen('curl -4 ip.sb')
            loc_ipv4 = res.read().strip('\n')
            a = input(f'{loc_ipv4} ? (y/n)')
            if a == 'n':
                loc_ipv4 = input("输入本地IPv4：")
                break
        node_info = sql3.execute('select * from node where id=?', node_id)
        try:
            f0 = open('./private_key', 'r')
            private_key = f0.read()
            f0.close()
        except:
            private_key = ''
        if private_key != '':
            f = open('./wgmod.conf', 'r')
            tmp_conf = f.read()
            f.close()
            tmp_conf = tmp_conf.replace('$private_key', private_key)
            tmp_conf = tmp_conf.replace('$ipv4', loc_ipv4)
            for item in node_info:
                tmp_conf = tmp_conf.replace('$node_key', item[4])
                tmp_conf = tmp_conf.replace('$node_ip', item[2])
                tmp_conf = tmp_conf.replace('$node_port', item[3])
            f1 = open('./wgmod_new.conf', 'w+')
            f1.write(tmp_conf)
            f1.close()
            os.system('rm /etc/wireguard/wg.conf')
            os.system('cp ./wgmod_new.conf /etc/wireguard/wg.conf')
            os.system('systemctl restart wg-quick@wg')
            print('等待检测结果')
            os.system('curl -4 ip.p3terx.com')
            a = input("已启用！回车继续")
            break
        else:
            a = input("请先添加您的私钥！回车继续")
            break


def private_key_add():
    while True:
        os.system('clear')
        private_key = input("private_key:")
        print(f'您的私钥：{private_key} ')
        choose = input('确认输入无误？ (y/n/q)')
        if choose == 'y' or choose == 'Y':
            f = open('./private_key', 'w')
            f.write(private_key)
            f.close()
            a = input('已添加！回车继续')
            break
        elif choose == 'q' or choose == 'Q':
            break
        else:
            pass


def menu():
    while True:
        os.system('clear')
        print("====== 一键配置 surfshark 出站脚本 ======")
        print("当前脚本仅测试了 ubuntu18+ ，使用脚本前建议先更新内核")
        print("surfshark 目前仅支持使用 ipv4 ， ipv6 暂不支持")
        print("0、安装 wireguard 组件")
        print("1、添加 wireguard 私钥")
        print("2、管理 surfshark 节点")
        print("3、使用 surfshark 出站")
        print("4、关闭 surfshark 出站")
        print("5、启用 开机自启动")
        print("6、关闭 开机自启动")
        print("Q、退出 surfshark 脚本")
        choose = input("请选择：")
        if choose == '0':
            os.system('apt install wireguard resolvconf -y')
        elif choose == '1':
            private_key_add()
        elif choose == '2':
            manage_surfshark_node()
        elif choose == '3':
            use_surfshark_out()
        elif choose == '4':
            os.system('systemctl stop wg-quick@wg')
            os.system('echo "nameserver 8.8.8.8 \n nameserver 8.8.4.4" >> /etc/resolv.conf')
            os.system('service networking restart')
            a = input('已关闭，是否要关闭开机自启动(y/n)：')
            if a == 'y':
                os.system('systemctl disable wg-quick@wg')
        elif choose == '5':
            os.system('systemctl enable wg-quick@wg')
            a = input('已启用，回车继续')
        elif choose == '6':
            os.system('systemctl disable wg-quick@wg')
            a = input('已停用，回车继续')
        elif choose == 'Q' or choose == 'q':
            break
        else:
            pass


if __name__ == '__main__':
    menu()