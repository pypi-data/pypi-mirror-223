# In[]
import sys, os
sys.path.append('../')
import numpy as np
import time
import torch
import matplotlib.pyplot as plt
import scipy.sparse as sps
from umap import UMAP
# import scmomat.model as model
# import scmomat.utils as utils
# import scmomat.bmk as bmk
# import scmomat.umap_batch as umap_batch
import scmomat

plt.rcParams["font.size"] = 10
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# In[]
data_dir = "../data/real/10x_pbmc/processed/"
CxR = sps.load_npz(data_dir + "RxC.npz").T
CxG = sps.load_npz(data_dir + "GxC.npz").T
RxG = sps.load_npz(data_dir + "GxR.npz").T
genes = np.loadtxt(data_dir + "genes.txt", dtype = object)
regions = np.loadtxt(data_dir + "regions.txt", dtype = object)

ncells = CxR.shape[0]
permute_idx = np.random.permutation(ncells)
chunk_size = int(ncells/3)
counts_rna = []
counts_atac = []
counts_rna.append(scmomat.preprocess(CxG[permute_idx[:chunk_size],:].toarray(), modality = "RNA", log = False))
counts_atac.append(scmomat.preprocess(CxR[permute_idx[:chunk_size],:].toarray(), modality = "ATAC"))
# counts_atac.append(None)

counts_rna.append(scmomat.preprocess(CxG[permute_idx[chunk_size:(2*chunk_size)],:].toarray(), modality = "RNA", log = False))
counts_atac.append(None)

counts_rna.append(None)
counts_atac.append(scmomat.preprocess(CxR[permute_idx[(2*chunk_size):],:].toarray(), modality = "ATAC"))

# CALCULATE PSEUDO-SCRNA-SEQ
counts_rna[2] = counts_atac[2] @ RxG
#BINARIZE, still is able to see the cluster pattern, much denser than scRNA-Seq (cluster pattern clearer)
counts_rna[2] = (counts_rna[2]!=0).astype(int)

counts = {"rna":counts_rna, "atac": counts_atac}
feats_name = {"rna": genes, "atac": regions}

counts["feats_name"] = feats_name
counts["nbatches"] = 3

# In[]
lamb = 0.001
batchsize = 0.1
# running seed
seed = 0
# number of latent dimensions
K = 30
interval = 1000
T = 4000
lr = 1e-2

start_time = time.time()
model1 = scmomat.scmomat_model(counts = counts, K = K, batch_size = batchsize, interval = interval, lr = lr, lamb = lamb, seed = seed, device = device)
losses1 = model1.train_func(T = T)
end_time = time.time()
print("running time: " + str(end_time - start_time))

x = np.linspace(0, T, int(T/interval)+1)
plt.plot(x, losses1)

# save the model
torch.save(model1, "10x_pbmc/" + f'CFRM_{K}_{T}.pt')


# In[]
# read in the ground truth labels

labels_batches = np.array(["multiomic"] * chunk_size + ["rna"] * chunk_size + ["atac"] * (ncells - 2* chunk_size), dtype = object)


# NOTE: Plot the result before post-processing
umap_op = UMAP(n_components = 2, n_neighbors = 30, min_dist = 0.2, random_state = 0) 
zs = model1.extract_cell_factors()
x_umap = umap_op.fit_transform(np.concatenate(zs, axis = 0))

scmomat.plot_latent(x_umap, annos = labels_batches, mode = "joint", save = "10x_pbmc/pre-process.png", figsize = (15,10), axis_label = "UMAP", markerscale = 6, s = 5, label_inplace = True)


# In[]
zs = model1.extract_cell_factors()

n_neighbors = 100
r = None
knn_indices, knn_dists = scmomat.calc_post_graph(zs, n_neighbors, njobs = 8, r = r)
x_umap = scmomat.calc_umap_embedding(knn_indices = knn_indices, knn_dists = knn_dists, n_components = 2, n_neighbors = n_neighbors, min_dist = 0.20, random_state = 0)

scmomat.plot_latent(x_umap, annos = labels_batches, mode = "joint", save = "10x_pbmc/post-process.png", figsize = (15,10), axis_label = "UMAP", markerscale = 6, s = 5, label_inplace = True)

# %%
