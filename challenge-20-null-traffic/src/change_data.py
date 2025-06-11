from scapy.all import *
randomized_mac_addresses = {}

def anonymize_mac_addresses(mac_address, typePacket):
    if typePacket == 0:
        return '00:00:00:31:32:75'
    else:
        return '00:00:00:83:d9:24'

def change_ip_addresses(ip_address, spoofwith):
    if not ip_address:
        return ip_address
    if not (ip_address in ["8.8.8.8","192.168.1.101","192.168.1.102"]):
        ip_address = spoofwith
    return ip_address



if __name__ == '__main__':
    pkts = rdpcap("backup.pcap")

    # Change your mac and ip addr
    for p in pkts:
        if p.haslayer('Ether'):
            layer = p[Ether]
            layer.src = anonymize_mac_addresses(layer.src, 0)
            layer.dst = anonymize_mac_addresses(layer.dst, 1)
        if p.haslayer('IP'):
            if p.haslayer('TCP'):
                tcp_layer = p[TCP]
                dst_port = tcp_layer.sport
                if dst_port > 500:
                    sourceIP = "17.34.15.169"
                    destinationIP = "46.176.132.191"
                else:
                    sourceIP = "46.176.132.191"
                    destinationIP = "17.34.15.169"
                layer = p[IP]
                layer.src = change_ip_addresses(layer.src, sourceIP)
                layer.dst = change_ip_addresses(layer.dst, destinationIP)


    wrpcap("new.pcap", pkts)