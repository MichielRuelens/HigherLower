import datetime

from ai.model_configs.base_model_config import BaseModelConfig
from ai.multi_layer_perceptron import MultiLayerPerceptron
from base.actions.action_service import ActionService
from base.game_state import GameState


class MLPConfig(BaseModelConfig):

    def __init__(self):
        # Model params
        self.hidden_units = [200, 200]
        # Environment params
        self.num_states = GameState.SIZE
        self.num_actions = ActionService().num_actions
        # Training params
        self.gamma = 0.99
        self.copy_step = 25
        self.print_exp_step = 100000000
        self.max_experiences = 10000
        self.min_experiences = 100
        self.batch_size = 32
        self.lr = 1e-2
        self.number_iterations = 1000
        self.epsilon = 0.99
        self.decay = 0.995
        self.min_epsilon = 0.1
        self.avg_rewards = 0

    @property
    def model_class(self):
        return MultiLayerPerceptron

    @property
    def log_dir(self) -> str:
        current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return 'logs/{}/{}'.format(self.name, current_time)

    @property
    def save_path(self) -> str:
        return "ai/models/{}".format(self.name())

    def name(self):
        return "MLPConfig"
