from netmiko import Netmiko

def connect_fortigate(fgt_host_addr, fgt_user, fgt_passwd, fgt_ssh_port=22):
    """
    Used to establish SSH connection to Fortigate appliances

    :param fgt_host_addr - Inform destination hostname (FQDN or IP addresses are supported)
    :param fgt_user - Inform username to connect in fortigate appliance
    :param fgt_passwd - Password is implemented by encrypted file, need to use fgt_encrypt_msg.py to generate

    Return a fortigate session
    """

    fortigate = {
        'device_type': 'fortinet',
        'host': fgt_host_addr,
        'port': fgt_ssh_port,
        'username': fgt_user,
        'password': fgt_passwd,
        'encoding': 'utf-8',
    }

    print(f"{' ---> Conectando em appliance(s)'}")
    net_connect = Netmiko(**fortigate)  # Conecta no firewall
    fw_hostname = net_connect.find_prompt()  # Captura hostname do ativo
    print(f"{' ---> Conectado em'} {fw_hostname[:-2]}")

    return net_connect


def detect_passive_node(fgt_session):
    """
    Used to detect passive nodes in cluster. This is necessary for backup passive nodes using active node as a jump host.
    As cluster index changes dynamically based on failover or switchover, this function detect actual passive nodes.

    :param fgt_session - Inform fortigate session

    Return a list with all passive nodes in cluster with this format:
    [[hostname1, serial_number1, cluster_index1], [hostname2, serial_number2, cluster_index2], ...]
    """

    # ---> Module starts here
    temp_file = open('./logging/temp.log', 'w')

    '''
    Detecting cluster index
    '''
    #  Getting cluster index from firewall
    fgt_cluster = fgt_session.send_command('get sys ha status | grep "HA cluster index"')

    #  Removing unwanted words
    replace_list = ['Primary', 'Secondary', 'HA cluster index', ':', '=', ' ']

    for i in range(0, len(replace_list)):
        fgt_cluster = fgt_cluster.replace(replace_list[i], '')

    #  Write data in txt file to treat
    temp_file.write(fgt_cluster)

    #  Open txt file in read mode
    temp_file = open('./logging/temp.log', 'r')

    fgt_clus_node = list()
    for line in temp_file:
        staging_var = line.split(',')  # put all nodes of cluster information in a temporary list to treat
        fgt_clus_node.append(staging_var[:])  # copy information of temp list to list with cluster information

    del (staging_var)  # deleting staging variable

    fgt_clus_node.sort(key=lambda id: id[2])  # Sorting list based on cluster index
    fgt_clus_info = [[x, y, z.strip()] for x, y, z in fgt_clus_node]  # Removing spaces


    #  Detecting active node hostname
    hostname = dectect_hostname(fgt_session)

    fgt_clus_index = list()  # list of passive nodes index

    #  Create a filtered list with only passive nodes
    for i in fgt_clus_info:
        if hostname != i[0]:
            fgt_clus_index.append(i[:])

    #  Return a list with passive nodes
    return fgt_clus_index


def dectect_hostname(fgt_session):
    """
    Used to detect the hostname of each appliances.

    :param fgt_session - Inform fortigate session

    Return a hostname of the appliance
    """

    #  Detecting active node hostname
    hostname = fgt_session.find_prompt()
    hostname = hostname[:-2]

    return hostname


def change_password(fgt_session, username, new_pwd):
    #  Command list
    #fgt_chg_pwd = ['config sys admin', 'edit ' + username, 'set password ' + new_pwd, 'end']

    #  Change password
    fgt_session.send_command_timing('config sys admin')
    fgt_session.send_command_timing('edit ' + username)
    fgt_session.send_command_timing('set password ' + new_pwd)
    fgt_session.send_command_timing('end')

