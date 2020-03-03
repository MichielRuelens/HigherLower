from typing import Dict, Any

import tensorflow as tf


class MultiLayerPerceptron(tf.keras.Model):
    def __init__(self, num_states, num_hidden_units, num_actions):
        super(MultiLayerPerceptron, self).__init__()
        self.input_layer = tf.keras.layers.InputLayer(input_shape=(num_states,))
        self.hidden_layers = []
        for i in num_hidden_units:
            self.hidden_layers.append(tf.keras.layers.Dense(i, activation='tanh', kernel_initializer='RandomNormal'))
        self.output_layer = tf.keras.layers.Dense(
            num_actions, activation='linear', kernel_initializer='RandomNormal')

    @tf.function
    def call(self, inputs: Dict[str, Any]):
        state = inputs['state']
        z = self.input_layer(state)
        for layer in self.hidden_layers:
            z = layer(z)
        output = self.output_layer(z)
        return output
