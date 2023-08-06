
import tensorflow as tf
from tensorflow.keras.layers import Layer

class CustomPoolingLayer(Layer):
    def __init__(self, call_function, compute_output_shape_function=None, **kwargs):
        super(CustomPoolingLayer, self).__init__(**kwargs)
        self._call_function = call_function
        self._compute_output_shape_function = compute_output_shape_function

    def call(self, inputs, training=None):
        return self._call_function(inputs)

    def compute_output_shape(self, input_shape):
        if self._compute_output_shape_function:
            return self._compute_output_shape_function(input_shape)
        else:
            # If compute_output_shape_function is not provided, infer output shape from the call function
            output_shape = self._call_function(tf.zeros(input_shape))
            return output_shape.shape

    def get_config(self):
        config = super(CustomPoolingLayer, self).get_config()
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)
