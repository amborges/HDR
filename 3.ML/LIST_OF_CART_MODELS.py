#!/usr/bin/env python3

# CART -- DECISION TREE


def name_model(model_attributes_list):
	CRITERION, SPLITTER, MAX_DEPTH, MIN_SAMPLES_SPLIT, MIN_SAMPLES_LEAF, MAX_FEATURES, MAX_LEAF_NODES, MIN_IMPURITY_DECREASE, CPP_ALPHA = model_attributes_list
	
	#substituindo o None por N
	MAX_DEPTH      = 'N' if MAX_DEPTH      is None else str(MAX_DEPTH)
	MAX_FEATURES   = 'N' if MAX_FEATURES   is None else str(MAX_FEATURES)
	MAX_LEAF_NODES = 'N' if MAX_LEAF_NODES is None else str(MAX_LEAF_NODES)
	
	#Limitando tamanho máximo de valores float
	MIN_IMPURITY_DECREASE = "{:.2f}".format(MIN_IMPURITY_DECREASE)
	CPP_ALPHA             = "{:.2f}".format(CPP_ALPHA)
	
	#Transformando inteiros em texto
	MIN_SAMPLES_SPLIT = str(MIN_SAMPLES_SPLIT)
	MIN_SAMPLES_LEAF  = str(MIN_SAMPLES_LEAF)
		
	#Convertendo os valores em código-texto
	model_name = "c{:s}_s{:s}_md{:s}_mss{:s}_msl{:s}_mf{:s}_mln{:s}_mid{:s}_ca{:s}".format(
		CRITERION, 
		SPLITTER,
		MAX_DEPTH, 
		MIN_SAMPLES_SPLIT, 
		MIN_SAMPLES_LEAF,
		MAX_FEATURES,
		MAX_LEAF_NODES,
		MIN_IMPURITY_DECREASE,
		CPP_ALPHA
	)
	return model_name


#The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “log_loss” and “entropy” both for the Shannon information gain, see Mathematical formulation.
CRITERION = ['gini', 'entropy']


#The strategy used to choose the split at each node. Supported strategies are “best” to choose the best split and “random” to choose the best random split
SPLITTER = ['best', 'random']

#The maximum depth of the tree. If None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.
MAX_DEPTH = [None, 3, 5, 7, 11, 13, 17, 19, 23]


#The minimum number of samples required to split an internal node: If int, then consider min_samples_split as the minimum number. (2 ou mais)
MIN_SAMPLES_SPLIT = [2, 3, 5, 7, 11, 13, 17, 19, 23]


#The minimum number of samples required to be at a leaf node. A split point at any depth will only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches. This may have the effect of smoothing the model, especially in regression. If int, then consider min_samples_leaf as the minimum number.
MIN_SAMPLES_LEAF = [1, 3, 5, 7, 11, 13, 17, 19, 23]


#The number of features to consider when looking for the best split: If “sqrt”, then max_features=sqrt(n_features). If “log2”, then max_features=log2(n_features). If None, then max_features=n_features.
MAX_FEATURES = ['sqrt', 'log2', None]


#Grow a tree with max_leaf_nodes in best-first fashion. Best nodes are defined as relative reduction in impurity. If None then unlimited number of leaf nodes.
MAX_LEAF_NODES = [None, 3, 5, 7, 11, 13, 17, 19, 23]


#A node will be split if this split induces a decrease of the impurity greater than or equal to this value. (detalhes da divisão no site)
MIN_IMPURITY_DECREASE = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


#Complexity parameter used for Minimal Cost-Complexity Pruning. The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen. By default, no pruning is performed. See Minimal Cost-Complexity Pruning for details. (valores float positivos) 
CPP_ALPHA = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]



THIS_LIST = [ (a, b, c, d, e, f, g, h, i)
              for a in CRITERION
              for b in SPLITTER
              for c in MAX_DEPTH
              for d in MIN_SAMPLES_SPLIT
              for e in MIN_SAMPLES_LEAF
              for f in MAX_FEATURES
              for g in MAX_LEAF_NODES
              for h in MIN_IMPURITY_DECREASE
              for i in CPP_ALPHA
            ]

