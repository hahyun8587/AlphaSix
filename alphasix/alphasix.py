import sys
import tensorflow as tf
from alphasix.alphasixsimulator import AlphaSixSimulator
from tools.AlphaZero.alphazero.agent import Agent
from tools.AlphaZero.alphazero.model import AlphaZeroModel

"""Configurations of alphasix.

Alphasix training configuration
* `40` steps of generating data and training
* Generates `512 * n_gpu` episodes per step
* `800` simulations for mcts
* Replay buffer size of `4 * n_episode`
* Trains for `1` epoch per step
* Samples `256 * n_gpu` examples per step
* Local batch size of `32`
* Alpha of `0.00002`
* Epsilon of `0.25`
* Saves model for every `5` steps

Alphasix neural network architecture
* 4 residual blocks
* 64 filters for convolutional block and residual blocks
"""

def main(argc: int, argv: list) -> None:
    if (argc == 1 or (argc == 2 and argv[1] == "-ap") 
            or (argv[1] != "-tr" and argv[1] != "-ap")):
        print("usage: python alphasix.py -tr [path/to/saved/model]\n\t\t \
               python alphasix.py -ap path/to/saved/model")

        return 
    
    SIMULATIONS = 800
        
    if argv[1] == "-tr": 
        strategy = tf.distribute.MirroredStrategy(
                ["GPU:0", "GPU:1", "GPU:2", "GPU:3"])
        
        STEPS = 40
        EPISODES = 512 * strategy.num_replicas_in_sync
        REPLAY_BUFFER_SIZE = 4 * EPISODES
        EPOCHS = 1
        EXAMPLES = 256 * strategy.num_replicas_in_sync
        LOCAL_BATCH_SIZE = 32
        GLOBAL_BATCH_SIZE = LOCAL_BATCH_SIZE * strategy.num_replicas_in_sync 
        #ALPHA = 0.00002
        #EPSILON = 0.25
        SAVE_STEPS = 5
        
        N_RES = 4
        N_FILTER = 64
        
        model = None
        
        if argc == 2:
            with strategy.scope():
                model = AlphaZeroModel(n_res=N_RES, n_filter=N_FILTER, 
                                       p_head_out_dim=64980, 
                                       input_shape=(2, 19, 19))
                model.compile_from_config(model.get_compile_config(STEPS, EPOCHS))
        else: 
            with strategy.scope():
                model = tf.keras.models.load_model(argv[2])
            
        agent = Agent(model, AlphaSixSimulator(19, 5), 1)
        agent.train(steps=STEPS, episodes=EPISODES, 
                    replay_buffer_size=REPLAY_BUFFER_SIZE, examples=EXAMPLES,
                    mini_batch_size=GLOBAL_BATCH_SIZE, save_steps=SAVE_STEPS)
    else:
        agent = Agent(tf.keras.models.load_model(argv[2]), 
                      AlphaSixSimulator(19, 5), 1)
        #agent.apply()


main(len(sys.argv), sys.argv)
