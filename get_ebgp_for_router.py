import sys

router_ips = {}
router_ips["MUNI"] = ["179.1.3.68", "179.1.3.65", 65, "MILA"]
router_ips["BASE"] = ["179.1.5.68", "179.1.5.66", 66, "LYON"]
router_ips["LUGA"] = ["179.1.9.2", "179.1.9.1", 67, "LUGA"]
router_ips["MILA"] = ["179.1.11.1", "179.1.11.2", 69, "MUNI"]
router_ips["LYON"] = ["179.1.10.1", "179.1.10.2", 70, "BASE"]
router_ips["VIEN"] = ["180.123.0.68", "180.123.0.123", 123, ""]

router_lo = {
    "ZURI": "68.151.0.1",
    "BASE": "68.152.0.1",
    "GENE": "68.153.0.1",
    "LUGA": "68.154.0.1",
    "MUNI": "68.155.0.1",
    "LYON": "68.156.0.1",
    "VIEN": "68.157.0.1",
    "MILA": "68.158.0.1"
}

def get_ebgp(router):
    ip68, ipo, gid, routero = router_ips[router]
    cmd = "./goto.sh %s router\n" % (router)
    cmd += "conf t\n"
    if router != "VIEN":
        cmd += "interface ext_%d_%s\n" % (gid, routero)
    else:
        cmd += "interface ixp_123\n"
    cmd += "ip address %s\n" % (ip68 + "/24")
    cmd += "q\n"
    cmd += "router bgp 68\n"
    cmd += "neighbor %s remote-as %d\n" % (ipo, gid)
    cmd += "q\n"
    cmd += "route-map ACCEPT_ALL permit 10\n"
    cmd += "q\n"
    cmd += "router bgp 68\n"
    cmd += "neighbor %s route-map ACCEPT_ALL in\n" % (ipo)
    cmd += "neighbor %s route-map ACCEPT_ALL out\n" % (ipo)
    cmd += "network 68.0.0.0/8\n"
    cmd += "q\n"
    cmd += "ip route 68.0.0.0/8 Null0\n"
    cmd += "router bgp 68\n"
    for each in router_lo:
        if each != router:
            cmd += "neighbor %s next-hop-self\n" % (router_lo[each])
    cmd += "q\nq\nq\n\n"
    return cmd


# router = sys.argv[1]
# print(get_ebgp(router))
for i in router_ips:
    print(get_ebgp(i))
