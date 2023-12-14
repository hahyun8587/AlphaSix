import sys
import tensorflow as tf
from tools.AlphaZero.alphazero.agent import Agent
from tools.AlphaZero.alphazero.model import AlphaZeroModel, AlphaZeroLoss
from .alphasixsimulator import AlphaSixSimulator
from .alphasixenvironment import AlphaSixEnvironment
from .alphasixagent import AlphaSixAgent

def main(argc: int, argv: list):
    model = AlphaZeroModel(n_res=6, p_head_out_dim=64980, 
                           input_shape=(2, 19, 19))
    
    model.compile(optimizer='adam', loss=AlphaZeroLoss())
    
    agent = AlphaSixAgent(model, AlphaSixSimulator(), 64980, 1)
    
    if argv[1] == '-tr':
        agent.train(steps=5000, n_ep_train=32, batch_size=128, 
                    n_train_save=32, n_replay_ep=128)
    elif argv[1] == '-app':
        if argc < 5:
            print('usage: {argv[0]} -app <ip> <port> <color>')
            
        agent.apply(AlphaSixEnvironment(19), argv[2], int(argv[3]), argv[4])

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
    