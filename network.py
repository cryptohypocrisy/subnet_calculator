# class used to instantiate a network object from an IP address, netmask, and
# corresponding CIDR notation value; can perform various calculations using
# these private attributes; best used with getipinfo.py module to get and return
# ip and mask as lists

import math as m


class Network:
    # ip and mask should be passed as lists containing four integers --
    # one for each octet in decimal form
    def __init__(self, ip_list=None, mask_list=None, cidr=0):
        self.__ip = ip_list
        self.__mask = mask_list
        self.__cidr = cidr

    # override default __str__ method for easy testing/viewing of
    # object's stored ip/mask/cidr values
    def __str__(self):
        ip_str = ""
        netmask_str = ""

        n = 0  # used to find the correct index if there are duplicate integers
        for octet in self.__ip:
            ip_str += str(octet)
            # don't print a dot if it's the last octet
            if self.__ip.index(octet, n) != len(self.__ip)-1:
                ip_str += "."
            n += 1

        n = 0  # used to find the correct index if there are duplicate integers
        for octet in self.__mask:
            netmask_str += str(octet)
            # don't print a dot if it's the last octet
            if self.__mask.index(octet, n) != len(self.__mask)-1:
                netmask_str += "."
            n += 1

        return "IP: " + ip_str + "\\" + str(self.__cidr) + "\n" + "Netmask: " + \
               netmask_str

    @property
    def ip(self):
        return tuple(self.__ip)

    @property
    def mask(self):
        return tuple(self.__mask)

    @property
    def cidr(self):
        return self.__cidr

    # AND the ip and mask octets to get the network address and return
    # it as a list
    def get_network_address(self):
        net_address_list = []

        for i in range(4):
            net_address = int(self.__ip[i]) & int(self.__mask[i])
            net_address_list.append(str(net_address))

        return tuple(net_address_list)

    # OR the ip and wildcard octets to get the broadcast address and
    # return it as a list
    def get_broadcast_address(self):
        broadcast_address_list = []
        wildcard_list = []

        # find wildcard octets by subtracing mask values from 255
        for n in self.__mask:
            x = 255 - int(n)
            wildcard_list.append(x)

        for i in range(4):
            broad_address = int(self.__ip[i]) | int(wildcard_list[i])
            broadcast_address_list.append(str(broad_address))

        return tuple(broadcast_address_list)

    # get the number of available networks and hosts
    def get_num_networks_hosts(self):
        for i in self.__mask:
            # the significant octet will be the first one with a value
            # below 255, iterate thru the mask octets until it is found
            if 0 <= int(i) < 255:
                significant_index = self.__mask.index(str(i))
                break
            else:
                # if all octets are 255 this will catch it
                significant_index = 3

        # use the cidr value to find number of hosts and number of networks
        # based on which octet is significant
        if significant_index == 0:
            number_of_networks = int(m.pow(2, self.__cidr))
        elif significant_index == 1:
            number_of_networks = int(m.pow(2, self.__cidr - 8))
        elif significant_index == 2:
            number_of_networks = int(m.pow(2, self.__cidr - 16))
        elif significant_index == 3:
            number_of_networks = int(m.pow(2, self.__cidr - 24))
            
        number_of_hosts = int(m.pow(2, 32 - self.__cidr) - 2)

        if int(self.__mask[3]) == 255:
            number_of_networks = 1
            number_of_hosts = 1

        return number_of_networks, number_of_hosts

    # use the first octet of the ip to find network class
    def get_net_class(self):
        if '0' <= self.__ip[0] <= '126':
            return "A"
        elif self.__ip[0] == '127':
            return "A (loopback)"
        elif '128' <= self.__ip[0] <= '191':
            return "B"
        elif '192' <= self.__ip[0] <= '223':
            return "C"
        elif '224' <= self.__ip[0] <= '239':
            return "D"
        else:
            return "E"

    # XOR each mask octet with 255 to get wildcard mask
    def get_wildcard(self):
        wildcard_list = []

        for octet in self.__mask:
            wildcard = int(octet) ^ 255
            wildcard_list.append(str(wildcard))

        return tuple(wildcard_list)
