"""Initialize modules."""
from .Heartbeat import Heartbeat
from .BaseHealthCheck import BaseHealthCheck

def init(config, uuclient):

    def cmd_heartbeat(dto_in):
        uucmd = config["uuApp"]['uuCmdList']['gatewayHeartbeat']
        resp, err = uuclient.post(uucmd, dto_in)
        return resp

    gateway_config = config["gateway"]

    return [Heartbeat(cmd_heartbeat)]

