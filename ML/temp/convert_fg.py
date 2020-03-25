import tensorflow as tf
from tensorflow.python.compiler.tensorrt import trt_convert as trt
with tf.Session() as sess:
    # First deserialize your frozen graph:
    with tf.gfile.GFile("/ml/data/ssd_v2_fg.pb",'rb') as f:
        frozen_graph = tf.GraphDef()
        frozen_graph.ParseFromString(f.read())
        # Now you can create a TensorRT inference graph from your
        # frozen graph:
        converter = trt.TrtGraphConverter(
    	    input_graph_def=frozen_graph,
    	    nodes_blacklist=["detection_scores","detection_classes","detection_boxes","num_detections"])
        #output nodes
        print('convert')
        trt_graph = converter.convert()
        converter.save('/ml/data/fg_convert/')
        
        # Import the TensorRT graph into a new graph and run:
        print('finish')
        tf.import_graph_def(trt_graph,input_map,return_elements=["detection_scores","detection_classes","detection_boxes","num_detections"])  #deserialize data add
        with tf.Session(graph=trt_graph) as sess:
            sess.run()
