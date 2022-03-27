#!/usr/bin/python
#
# Copyright 6WIND, 2017
#

from __future__ import print_function
from pyrad import dictionary, packet, server
import sys
from opencoa_api.config import Config

config = Config(RADIUS_DICTIONARY_PATH="opencoa_api/attributes")


class FakeCoA(server.Server):
    def HandleCoaPacket(self, pkt):
        """Accounting packet handler.
        Function that is called when a valid
        accounting packet has been received.
        :param pkt: packet to process
        :type  pkt: Packet class instance
        """
        print("Received a coa request %d" % pkt.code)
        print("  Attributes: ")
        for attr in pkt.keys():
            print("  %s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        # try ACK or NACK
        # reply.code = packet.CoANAK
        if "Framed-IP-Netmask" in pkt.keys():
            reply.code = packet.CoANAK
        else:
            reply.code = packet.CoAACK
        self.SendReplyPacket(pkt.fd, reply)

    def HandleDisconnectPacket(self, pkt):
        print("Received a disconnect request %d" % pkt.code)
        print("  Attributes: ")
        for attr in pkt.keys():
            print("  %s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        # try ACK or NACK
        # reply.code = packet.DisconnectNAK
        reply.code = packet.DisconnectACK
        self.SendReplyPacket(pkt.fd, reply)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: client-coa.py 3799")
        sys.exit(1)

    bindport = int(sys.argv[1])

    config.load_dictionary()

    # create server/coa only and read dictionary
    # bind and listen only on 0.0.0.0:argv[1]
    coa = FakeCoA(
        addresses=["127.0.0.1"],
        dict=config.RADIUS_DICTIONARY,
        coaport=bindport,
        auth_enabled=False,
        acct_enabled=False,
        coa_enabled=True,
    )

    # add peers (address, secret, name)
    coa.hosts["127.0.0.1"] = server.RemoteHost("127.0.0.1", b"mysecret", "localhost")

    # start
    coa.Run()
