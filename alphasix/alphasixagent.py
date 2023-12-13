import numpy as np
from tools.AlphaZero.alphazero.environment import Environment
from ..tools.AlphaZero.alphazero.agent import Agent
from ..tools.AlphaZero.alphazero.node import Node

class AlphaSixAgent(Agent):
    
    def apply(self, env: Environment, ip: str, port: int, color: str) -> None:
        init_s = env.gen_init_s(ip, port, color)     
        
        if color == 'BALCK':
            a = env.response(-1)
            root_s = self._simulator.simulate(init_s, a)
        else:
            env.response(-2)
            root_s = init_s
        
        root_p, root_v = self._model(root_s[np.newaxis, :], False)
        root_p = root_p.numpy().reshape(-1)
        root_v = root_v[0][0]
        root = Node(root_s, root_v, root_p, False)
        
        while 1:
            pi = root.mcts()
            a = env.response(np.random.choice(self._n_a, p=pi))
            
            if a == -2:
                break
            
            child = root.get_child(a)
            
            if child is None:
                root_s = self._simulator.simulate(init_s, a)
                root_p, root_v = self._model(root_s[np.newaxis, :], False)
                root_p = root_p.numpy().reshape(-1)
                root_v = root_v[0][0]
                root = Node(root_s, root_v, root_p, False)
            else:
                root = child
    
        