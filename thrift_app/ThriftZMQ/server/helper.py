import os

def get_env_tf(gpu_id, mem_fraction):
    import tensorflow as tf
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = mem_fraction
    graph = tf.Graph()
    sess = tf.Session(config=config, graph=graph)
    return tf, sess, graph





        