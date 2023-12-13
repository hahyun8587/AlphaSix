import sys
import tensorflow as tf
from tools.AlphaZero.alphazero.agent import Agent
from tools.AlphaZero.alphazero.model import AlphaZeroModel, AlphaZeroLoss
from .alphasixsimulator import AlphaSixSimulator

def main(argc: int, argv: list):
    model = AlphaZeroModel(n_res=19, p_head_out_dim=64980, 
                           input_shape=(2, 19, 19))
    
    model.compile(optimizer='adam', loss=AlphaZeroLoss())
    
    agent = Agent(model, AlphaSixSimulator(), 64980, 1)
    
    agent.train(steps=5000, n_ep_train=2000, batch_size=1024, 
                n_train_save=500, n_replay_ep=8000)


if __name__ == '__main__':
    
    main(len(sys.argv), sys.argv)
    