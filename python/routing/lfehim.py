import logging
from network.network import Network
from network.node import Node
from routing_protocol import RoutingProtocol
import config as cf
from python.utils import *

class LFEHIM(RoutingProtocol):
    def _setup_phase(self, network):
        # type: (Network) -> None
        logging.debug("LFEHIM: setup phase")
        sensor_nodes = network.get_sensor_nodes()

        logging.debug("LFEHIM: Sending hello packets")
        for node in sensor_nodes:
            node.next_hop(cf.MIN_RADIUS)
            if node._next_hop == None:
                logging.debug("LFEHIM: No neighbours; increase tx range")
                node.next_hop(cf.MAX_RADIUS)
                    if node._next_hop == None:
                        node.alive = 0
                        node.time_of_death = network.round


        logging.debug("LFEHIM: Finding Best Forwarder")
        alive_sensor_nodes = network.get_alive_nodes()
        
        for node in alive_sensor_nodes:
            other_nodes = alive_sensor_nodes[:].remove(node)
            min_depth_node=min(other_nodes,key= lambda node: node.pos_d)
            other_min_depth_nodes = filter(lambda node: node.pos_d == min_depth_node.pos_d, other_nodes)
            if len(other_min_depth_nodes) != 1:
                logging.debug("LFEHIM: Multiple forwarders with min pressure level")
                m_calculate_distance = lambda mnode: calculate_distance(node,mnode)
                min_depth_node = min(other_min_depth_nodes, key=m_calculate_distance)
            node.next_hop(min_depth_node)
