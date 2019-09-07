from ThriftApp.ThriftZMQ.server.helper import get_env_tf
from ThriftApp.ThriftZMQ.server.handler_base import ModelBase
import numpy as np


class Model(ModelBase):
    def __init__(self, gpu_id, mem_fraction):
        super().__init__()
        print("Init Handler -- gpu_id: {} -- mem_fraction: {}".format(gpu_id, mem_fraction))
        self.tf, self.sess, self.graph = get_env_tf(gpu_id, mem_fraction)
        self._load_graph()

    def _load_graph(self):
        with self.graph.as_default():
            self.a = self.tf.placeholder(dtype=self.tf.int32, shape=(None, 1))
            self.c = 2*self.a

    def process(self, list_input_dict):
        inputs = []
        for input_dict in list_input_dict:
            inputs.append(input_dict['input'])
        inputs = np.array(inputs)
        inputs = np.reshape(inputs, [len(inputs), 1])
        with self.graph.as_default():
            c = self.sess.run(self.c, feed_dict={self.a: inputs})
        return c
