import pdb
import time
import numpy as np
import copy

from .util_ import procrustes, print_log, nearest_neighbors, sparse_matrix, lexargmax
from .global_reg_ import procrustes_init, spectral_alignment, ltsa_alignment, sdp_alignment, procrustes_final, rgd_alignment, gpm_alignment, compute_alignment_err, compute_far_off_points

import scipy
from scipy.linalg import svdvals
from scipy.sparse.csgraph import minimum_spanning_tree, breadth_first_order, laplacian, connected_components
from scipy.sparse import coo_matrix, csr_matrix, triu
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import pdist, cdist, squareform
from matplotlib import pyplot as plt

import multiprocess as mp

class GlobalViews:
    def __init__(self, exit_at, print_logs=True, debug=False):
        self.exit_at = exit_at
        self.print_logs = print_logs
        self.debug = debug
        
        self.y_init = None
        self.color_of_pts_on_tear_init = None
        self.y_final = None
        self.color_of_pts_on_tear_final = None
        self.tracker = {}
        
        self.local_start_time = time.time()
        self.global_start_time = time.time()
        
        # saved only when debug is True
        self.n_Utilde_Utilde = None
        self.seq_of_intermed_views_in_cluster = None
        self.parents_of_intermed_views_in_cluster = None
        self.y_seq_init = None
        self.y_spec_init = None
        self.Utilde_t = None
        self.y_refined_at = []
        self.color_of_pts_on_tear_at = []
        
    def log(self, s='', log_time=False):
        if self.print_logs:
            self.local_start_time = print_log(s, log_time,
                                              self.local_start_time, 
                                              self.global_start_time)
            
    def fit(self, d, d_e, Utilde, C, c, n_C, intermed_param, global_opts, vis, vis_opts):
        print('Using', global_opts['align_transform'], 'transforms for alignment.')
        if global_opts['align_transform'] == 'rigid':
            # Compute |Utilde_{mm'}|
            n_Utilde_Utilde = Utilde.dot(Utilde.transpose())
            n_Utilde_Utilde.setdiag(0)
            
            # Compute sequence of intermedieate views
            seq_of_intermed_views_in_cluster, \
            parents_of_intermed_views_in_cluster, \
            cluster_of_intermed_view = self.compute_seq_of_intermediate_views(Utilde, n_C, 
                                                                             n_Utilde_Utilde,
                                                                             intermed_param, global_opts)
            
            if global_opts['add_dim']:
                intermed_param.add_dim = True
                d = d + 1
            # Visualize embedding before init
            if global_opts['vis_before_init']:
                self.vis_embedding_(d, intermed_param, C, Utilde,
                                  n_Utilde_Utilde, global_opts, vis,
                                  vis_opts, title='Before_Init')
            
            # Compute initial embedding
            y_init, color_of_pts_on_tear_init = self.compute_init_embedding(d, d_e, Utilde, n_Utilde_Utilde, intermed_param,
                                                                            seq_of_intermed_views_in_cluster,
                                                                            parents_of_intermed_views_in_cluster,
                                                                            C, c, vis, vis_opts, global_opts)

            self.y_init = y_init
            self.color_of_pts_on_tear_init = color_of_pts_on_tear_init
            
            if global_opts['refine_algo_name']:
                y_final,\
                color_of_pts_on_tear_final = self.compute_final_embedding(y_init, d, d_e, Utilde, C, c, intermed_param,
                                                                          n_Utilde_Utilde,
                                                                          seq_of_intermed_views_in_cluster,
                                                                          parents_of_intermed_views_in_cluster, 
                                                                          cluster_of_intermed_view, global_opts,
                                                                          vis, vis_opts)
                self.y_final = y_final
                self.color_of_pts_on_tear_final = color_of_pts_on_tear_final
            
        elif global_opts['align_transform'] == 'affine':
            # TODO
            print('TODO: Need to implement', flush = True)
#             self.y_final = self.compute_final_global_embedding_ltsap_based()
#             self.color_of_pts_on_tear_final = None
        
        
        
        if self.debug:
            self.n_Utilde_Utilde = n_Utilde_Utilde
            self.seq_of_intermed_views_in_cluster = seq_of_intermed_views_in_cluster
            self.parents_of_intermed_views_in_cluster = parents_of_intermed_views_in_cluster
            self.cluster_of_intermed_view = cluster_of_intermed_view
    
    # Motivated from graph lateration
    def compute_seq_of_intermediate_views(self, Utilde, n_C, n_Utilde_Utilde,
                                          intermed_param, global_opts, print_prop = 0.25):
        M = Utilde.shape[0]
        print_freq = int(print_prop * M)
        n_proc = global_opts['n_proc']
        self.log('Computing laterations scores for overlaps b/w intermed views')
        # W_{mm'} = W_{m'm} measures the ambiguity between
        # the pair of the embeddings of the overlap 
        # Utilde_{mm'} in mth and m'th intermediate views
        W_rows, W_cols = triu(n_Utilde_Utilde).nonzero()
        n_elem = W_rows.shape[0]
        W_data = np.zeros(n_elem)
        chunk_sz = int(n_elem/n_proc)
        def target_proc(p_num, q_):
            start_ind = p_num*chunk_sz
            if p_num == (n_proc-1):
                end_ind = n_elem
            else:
                end_ind = (p_num+1)*chunk_sz
            W_data_ = np.zeros(end_ind-start_ind)
            for i in range(start_ind, end_ind):
                m = W_rows[i]
                mpp = W_cols[i]
                Utilde_mmp = Utilde[m,:].multiply(Utilde[mpp,:]).nonzero()[1]
                # Compute V_{mm'}, V_{m'm}, Vbar_{mm'}, Vbar_{m'm}
                V_mmp = intermed_param.eval_({'view_index': m, 'data_mask': Utilde_mmp})
                V_mpm = intermed_param.eval_({'view_index': mpp, 'data_mask': Utilde_mmp})
                Vbar_mmp = V_mmp - np.mean(V_mmp,0)[np.newaxis,:]
                Vbar_mpm = V_mpm - np.mean(V_mpm,0)[np.newaxis,:]
                # Compute ambiguity as the minimum singular value of
                # the d x d matrix Vbar_{mm'}^TVbar_{m'm}
                svdvals_ = svdvals(np.dot(Vbar_mmp.T,Vbar_mpm))
                W_data_[i-start_ind] = svdvals_[-1]
            q_.put((start_ind, end_ind, W_data_))
        
        q_ = mp.Queue()
        proc = []
        for p_num in range(n_proc):
            proc.append(mp.Process(target=target_proc, args=(p_num,q_)))
            proc[-1].start()
        
        for p_num in range(n_proc):
            start_ind, end_ind, W_data_ = q_.get()
            W_data[start_ind:end_ind] = W_data_
        q_.close()
        
        for p_num in range(n_proc):
            proc[p_num].join()
        
        self.log('Done', log_time=True)
        self.log('Computing a lateration.')
        W = csr_matrix((W_data, (W_rows, W_cols)), shape=(M,M))
        W = W + W.T
        # Compute maximum spanning tree/forest of W
        T = minimum_spanning_tree(-W)
        n_comp = connected_components(T, directed=False, return_labels=False)
        
        # Remove edges to force clusters if desired
        if global_opts['n_forced_clusters'] > n_comp:
            inds = np.argsort(T.data)[-(global_opts['n_forced_clusters']-n_comp):]
            T.data[inds] = 0
            T.eliminate_zeros()
            
        
        # Detect clusters of manifolds and create
        # a sequence of intermediate views for each of them
        n_visited = 0
        seq_of_intermed_views_in_cluster = []
        parents_of_intermed_views_in_cluster = []
        # stores cluster number for the intermediate views in a cluster
        cluster_of_intermed_view = np.zeros(M,dtype=int)
        is_visited = np.zeros(M, dtype=bool)
        cluster_num = 0
        inf_zeta = np.max(intermed_param.zeta)+1
        rank_arr = np.zeros((M,3))
        rank_arr[:,1] = n_C
        rank_arr[:,2] = -intermed_param.zeta
        while n_visited < M:
            # First intermediate view in the sequence
            #s_1 = np.argmax(n_C * (1-is_visited))
            #s_1 = np.argmin(intermed_param.zeta +  inf_zeta*is_visited)
            rank_arr[:,0] = 1-is_visited
            s_1 = lexargmax(rank_arr)
            # Compute breadth first order in T starting from s_1
            s_, rho_ = breadth_first_order(T, s_1, directed=False) #(ignores edge weights)
            seq_of_intermed_views_in_cluster.append(s_)
            parents_of_intermed_views_in_cluster.append(rho_)
            is_visited[s_] = True
            cluster_of_intermed_view[s_] = cluster_num
            n_visited = np.sum(is_visited)
            cluster_num = cluster_num + 1
            
        self.log('Seq of intermediate views and their predecessors computed.')
        self.log('No. of connected components = ' + str(len(seq_of_intermed_views_in_cluster)))
        if len(seq_of_intermed_views_in_cluster)>1:
            self.log('Multiple connected components detected')
        self.log('Done.', log_time=True)
        return seq_of_intermed_views_in_cluster,\
               parents_of_intermed_views_in_cluster,\
               cluster_of_intermed_view
    
    # dist = y_d_e
    def compute_pwise_dist_in_embedding(self, intermed_param, Utilde, C, global_opts,
                                        y=None, dist=None, max_crossings=5, tol=1e-6):
        M,n = Utilde.shape
        assert ((y is not None) or (dist is not None))
        
        if dist is None:
            dist = squareform(pdist(y))

        n_Utilde_Utilde = Utilde.dot(Utilde.transpose())
        n_Utilde_Utilde.setdiag(False)
        Utildeg = self.compute_Utildeg(y, C, global_opts)
        n_Utildeg_Utildeg = Utildeg.dot(Utildeg.transpose())
        n_Utildeg_Utildeg.setdiag(False)

        # Compute the tear: a graph between views where ith view
        # is connected to jth view if they are neighbors in the
        # ambient space but not in the embedding space
        tear = n_Utilde_Utilde-n_Utilde_Utilde.multiply(n_Utildeg_Utildeg)
        # no tear then return dist
        if np.sum(tear)==0:
            return dist
        
        old_dist = dist.copy()
        for i_crossing in range(max_crossings):
            print('i_crossing:', i_crossing, flush=True)
            # Keep track of visited views across clusters of manifolds
            is_visited = np.zeros(M, dtype=bool)
            n_visited = 0
            pts_on_tear = np.zeros(n, dtype=bool)
            while n_visited < M: # boundary of a cluster remain to be colored
                s0 = np.argmax(is_visited == 0)
                seq, rho = breadth_first_order(n_Utilde_Utilde, s0, directed=False) #(ignores edge weights)
                is_visited[seq] = True
                n_visited = np.sum(is_visited)

                # Iterate over views
                for m in seq:
                    to_tear_mth_view_with = tear[m,:].nonzero()[1].tolist()
                    if len(to_tear_mth_view_with):
                        # Points in the overlap of mth view and the views
                        # on the opposite side of the tear
                        Utilde_m = Utilde[m,:]
                        for i in range(len(to_tear_mth_view_with)):
                            mpp = to_tear_mth_view_with[i]
                            temp_i = Utilde_m.multiply(Utilde[mpp,:])
                            # Compute points on the overlap of m and m'th view
                            # which are in mth cluster and in m'th cluster. If
                            # both sets are non-empty then assign them same color.
                            temp_m = C[m,:].multiply(temp_i).nonzero()[1]
                            temp_mpp = C[mpp,:].multiply(temp_i).nonzero()[1]

                            y_m_temp_m = intermed_param.eval_({'view_index': m, 'data_mask': temp_m})
                            y_m_temp_mpp = intermed_param.eval_({'view_index': m, 'data_mask': temp_mpp})
                            y_mpp_temp_m = intermed_param.eval_({'view_index': mpp, 'data_mask': temp_m})
                            y_mpp_temp_mpp = intermed_param.eval_({'view_index': mpp, 'data_mask': temp_mpp})

                            dist_m = cdist(y_m_temp_m, y_m_temp_mpp)
                            dist_mpp = cdist(y_mpp_temp_m, y_mpp_temp_mpp)
                            dist_ = np.minimum(dist_m, dist_mpp)

                            dist[np.ix_(temp_m,temp_mpp)] = dist_
                            dist[np.ix_(temp_mpp,temp_m)] = dist_.T
                            pts_on_tear[temp_m] = True
                            pts_on_tear[temp_mpp] = True

            # Compute min of original vs lengths of one hop-distances by
            # contracting dist.T, dist with min as the binary operation
            print('Computing min(original dist, min(one-hop distances))', flush=True)
            print('#pts on tear', np.sum(pts_on_tear))
    #         print_freq = int(n/10)
    #         for i in range(n):
    #             if np.mod(i, print_freq) == 0:
    #                 print('Processed', i, 'points.', flush=True)
    #             dist[i,:] = np.minimum(dist[i,:],np.min(dist[pts_on_tear,:] + dist[i,pts_on_tear][:,None], axis=0))

            n_proc = global_opts['n_proc']
            chunk_sz = int(n/n_proc)
            def target_proc(p_num, q_, dist, pts_on_tear):
                start_ind = p_num*chunk_sz
                if p_num == (n_proc-1):
                    end_ind = n
                else:
                    end_ind = (p_num+1)*chunk_sz
                dist_ = np.zeros((end_ind-start_ind,n))
                for i in range(start_ind, end_ind):
                    dist_[i-start_ind,:] = np.minimum(dist[i,:],np.min(dist[pts_on_tear,:] + dist[i,pts_on_tear][:,None], axis=0))
                q_.put((start_ind, end_ind, dist_))

            q_ = mp.Queue()
            proc = []
            for p_num in range(n_proc):
                proc.append(mp.Process(target=target_proc, args=(p_num,q_, dist, pts_on_tear)))
                proc[-1].start()

            for p_num in range(n_proc):
                start_ind, end_ind, dist_ = q_.get()
                dist[start_ind:end_ind,:] = dist_
            q_.close()

            for p_num in range(n_proc):
                proc[p_num].join()
            
            mean_abs_diff = np.mean(np.abs(dist-old_dist))
            print('Mean Absolute Difference in distances:', mean_abs_diff)
            if mean_abs_diff < tol:
                break
            old_dist = dist.copy()

        return dist
    
    def compute_color_of_pts_on_tear_heuristic(self, y, Utilde, C, global_opts,
                                                n_Utilde_Utilde, Utildeg=None):
        M,n = Utilde.shape

        # Compute |Utildeg_{mm'}| if not provided
        if Utildeg is None:
            Utildeg = self.compute_Utildeg(y, C, global_opts)

        color_of_pts_on_tear = np.zeros(n)+np.nan

        # Compute the tear: a graph between views where ith view
        # is connected to jth view if they are neighbors in the
        # ambient space but not in the embedding space
        # tear = Utilde -  Utilde.multiply(Utildeg)
        # tear = tear.dot(tear.T)
        tear = n_Utilde_Utilde - n_Utilde_Utilde.multiply(Utildeg.dot(Utildeg.T))
        tear.eliminate_zeros()
        # Keep track of visited views across clusters of manifolds
        is_visited = np.zeros(M, dtype=bool)
        n_visited = 0
        while n_visited < M: # boundary of a cluster remain to be colored
            # track the next color to assign
            cur_color = 1

            s0 = np.argmax(is_visited == 0)
            seq, rho = breadth_first_order(n_Utilde_Utilde, s0, directed=False) #(ignores edge weights)
            is_visited[seq] = True
            n_visited = np.sum(is_visited)

            # Iterate over views
            for m in seq:
                to_tear_mth_view_with = tear[m,:].nonzero()[1].tolist()
                if len(to_tear_mth_view_with):
                    # Points in the overlap of mth view and the views
                    # on the opposite side of the tear
                    Utilde_m = Utilde[m,:]
                    for i in range(len(to_tear_mth_view_with)):
                        mpp = to_tear_mth_view_with[i]
                        temp0 = np.isnan(color_of_pts_on_tear)
                        temp_i = Utilde_m.multiply(Utilde[mpp,:])
                        temp_m = C[m,:].multiply(temp_i).multiply(temp0)
                        temp_mp = C[mpp,:].multiply(temp_i).multiply(temp0)
                        if temp_m.sum():
                            color_of_pts_on_tear[(temp_m).nonzero()[1]] = cur_color
                            cur_color += 1
                        if temp_mp.sum():
                            color_of_pts_on_tear[(temp_mp).nonzero()[1]] = cur_color
                            cur_color += 1
        return color_of_pts_on_tear
    
    def compute_spectral_color_of_pts_on_tear(self, y, Utilde, C, global_opts,
                                     n_Utilde_Utilde, Utildeg=None, return_G_T=False):
        M,n = Utilde.shape
        max_diversity = np.max(global_opts['tear_color_eig_inds'])+1
        color_of_pts_on_tear = np.zeros((n, max_diversity)) + np.nan

        # Compute |Utildeg_{mm'}| if not provided
        if Utildeg is None:
            Utildeg = self.compute_Utildeg(y, C, global_opts)

        # Compute the tear: a graph between views where ith view
        # is connected to jth view if they are neighbors in the
        # ambient space but not in the embedding space
        # tear = Utilde -  Utilde.multiply(Utildeg)
        # tear = tear.dot(tear.T)
        tear_G0 = n_Utilde_Utilde.multiply(Utildeg.dot(Utildeg.T))
        tear_G1 = n_Utilde_Utilde - tear_G0
        tear_G1.eliminate_zeros()
        
        G1_row_inds = []
        G1_col_inds = []
        tear_G1_row, tear_G1_col = tear_G1.nonzero()
        if len(tear_G1_row) == 0:
            return color_of_pts_on_tear
        pts_on_tear = np.zeros(n, dtype=bool)
        for ind in range(len(tear_G1_row)):
            i = tear_G1_row[ind]
            j = tear_G1_col[ind]
            T_ij = Utilde[j,:].multiply(C[i,:]).nonzero()[1]
            T_ji = Utilde[i,:].multiply(C[j,:]).nonzero()[1]
            n_T_ij = len(T_ij)
            n_T_ji = len(T_ji)
            #pts_on_overlap = T_ij + T_ji
            #pts_on_overlap = pts_on_overlap.nonzero()[1]
            #n_ = len(pts_on_overlap)
            if (n_T_ij*n_T_ji) > 0:
                pts_on_tear[T_ij] = True
                pts_on_tear[T_ji] = True
                G1_row_inds += np.repeat(T_ij, n_T_ji).tolist()
                G1_col_inds += np.tile(T_ji, n_T_ij).tolist()
                G1_row_inds += np.repeat(T_ji, n_T_ij).tolist()
                G1_col_inds += np.tile(T_ij, n_T_ji).tolist()

        G1 = csr_matrix((np.ones(len(G1_row_inds)), (G1_row_inds, G1_col_inds)),
                        shape=(n,n), dtype=bool)
        
        G1 = G1[np.ix_(pts_on_tear,pts_on_tear)]
        pts_on_tear = np.where(pts_on_tear)[0]
        n_pts_on_tear = len(pts_on_tear)
        n_comp, labels = connected_components(G1, directed=False, return_labels=True)
        n_points_in_comp = []
        for i in range(n_comp):
            comp_i = labels==i
            n_points_in_comp.append(np.sum(comp_i))
        
        offset = np.zeros(max_diversity)
        if return_G_T:
            G_T_info = []
        for i in np.flip(np.argsort(n_points_in_comp)).tolist():
            comp_i = labels==i
            n_comp_i = np.sum(comp_i)
            scale = n_comp_i/n_pts_on_tear
            if n_comp_i <= max(3, int(global_opts['color_cutoff_frac']*n)):
                color_of_pts_on_tear[pts_on_tear[comp_i],:] = offset + scale/2
                offset += scale
                continue
            G1_comp_i = G1[np.ix_(comp_i, comp_i)]
            G1_comp_i = laplacian(G1_comp_i.astype('float')) # NOTE: Laplacian not adjacency
            if return_G_T:
                G_T_info.append([i, G1_comp_i])
            np.random.seed(42)
            v0 = np.random.uniform(0, 1, G1_comp_i.shape[0])
            n_eigs = min(n_comp_i, max_diversity)
            _, colors_ = scipy.sparse.linalg.eigsh(G1_comp_i, v0=v0,
                                                   k=n_eigs,
                                                   sigma=-1e-3)
            colors_max = np.max(colors_, axis=0)[None,:]
            colors_min = np.min(colors_, axis=0)[None,:]
            colors_ = (colors_-colors_min)/(colors_max-colors_min + 1e-12) # scale to [0,1]
            colors_ = offset[None,:n_eigs] + colors_*scale
            offset += scale
            color_of_pts_on_tear[np.ix_(pts_on_tear[comp_i],np.arange(n_eigs))] = colors_
            if global_opts['color_largest_tear_comp_only']:
                break
            
        if return_G_T:
            return color_of_pts_on_tear, [labels, G_T_info]
        else:
            return color_of_pts_on_tear
    
    def compute_color_of_pts_on_tear(self, y, Utilde, C, global_opts,
                                     n_Utilde_Utilde, Utildeg=None):
        if global_opts['tear_color_method'] == 'spectral':
            return self.compute_spectral_color_of_pts_on_tear(y, Utilde, C, global_opts,
                                                              n_Utilde_Utilde, Utildeg=Utildeg)
        else:
            return self.compute_color_of_pts_on_tear_heuristic(y, Utilde, C, global_opts,
                                                              n_Utilde_Utilde, Utildeg=Utildeg)
            
    
    def vis_embedding_(self, y, d, intermed_param, c, C, Utilde,
                      n_Utilde_Utilde, global_opts, vis,
                      vis_opts, title='', color_of_pts_on_tear=None,
                      Utilde_t=None):
        M,n = Utilde.shape
        if global_opts['color_tear']:
            if (color_of_pts_on_tear is None) and global_opts['to_tear']:
                color_of_pts_on_tear = self.compute_color_of_pts_on_tear(y, Utilde, C, global_opts,
                                                                         n_Utilde_Utilde)
            if global_opts['to_tear']:
                color_of_pts_on_tear = color_of_pts_on_tear[:,global_opts['tear_color_eig_inds']]
        else:
            color_of_pts_on_tear = None
            
        vis.global_embedding(y, vis_opts['c'], vis_opts['cmap_interior'],
                                  color_of_pts_on_tear, vis_opts['cmap_boundary'],
                                  title)
            
        # if color_of_pts_on_tear is not None:
        #     pts_on_tear = np.nonzero(~np.isnan(color_of_pts_on_tear))[0]
        #     y_ = []
        #     ind_ = []
        #     #color_of_pts_on_tear = np.zeros(n)+np.nan
        #     color_of_pts_on_tear_ = []
        #     for i in range(pts_on_tear.shape[0]):
        #         k = pts_on_tear[i]
        #         for m in Utilde[:,k].nonzero()[0].tolist():
        #             if m == c[k]:
        #                 continue
        #             y_.append(intermed_param.eval_({'view_index': m, 'data_mask': np.array([k])}))
        #             ind_.append(k)
        #             color_of_pts_on_tear_.append(color_of_pts_on_tear[k])
        #     ind_ = np.array(ind_)
        #     color_of_pts_on_tear_ = np.array(color_of_pts_on_tear_)
        #     if len(y_):
        #         y_ = np.concatenate(y_, axis=0)
        #         y_ = np.concatenate([y,y_], axis=0)
        #         color_of_pts_on_tear_ = np.concatenate([color_of_pts_on_tear, color_of_pts_on_tear_], axis=0)
        #         if vis_opts['c'] is not None:
        #             c_ = vis_opts['c'][ind_]
        #             c_ = np.concatenate([vis_opts['c'],c_], axis=0)
        #         else:
        #             c_ = None
        #         vis.global_embedding(y_,c_, vis_opts['cmap_interior'],
        #                               color_of_pts_on_tear_, vis_opts['cmap_boundary'],
        #                               title)
        #     else:
        #         vis.global_embedding(y, vis_opts['c'], vis_opts['cmap_interior'],
        #                           color_of_pts_on_tear, vis_opts['cmap_boundary'],
        #                           title)
        # else:
        #     vis.global_embedding(y, vis_opts['c'], vis_opts['cmap_interior'],
        #                           color_of_pts_on_tear, vis_opts['cmap_boundary'],
        #                           title)
        plt.show()
        return color_of_pts_on_tear, y
    
    def vis_embedding(self, y, vis, vis_opts, color_of_pts_on_tear=None, title=''):
        vis.global_embedding(y, vis_opts['c'], vis_opts['cmap_interior'],
                              color_of_pts_on_tear, vis_opts['cmap_boundary'],
                              title)
        plt.show()
        
    def add_spacing_bw_clusters(self, y, d, seq_of_intermed_views_in_cluster,
                                intermed_param, C):
        n_clusters = len(seq_of_intermed_views_in_cluster)
        if n_clusters == 1:
            return
        
        M,n = C.shape
            
        # arrange connected components nicely
        # spaced on horizontal (x) axis
        offset = 0
        for i in range(n_clusters):
            seq = seq_of_intermed_views_in_cluster[i]
            pts_in_cluster_i = np.where(C[seq,:].sum(axis=0))[1]
            
            # make the x coordinate of the leftmost point
            # of the ith cluster to be equal to the offset
            if i > 0:
                offset_ = np.min(y[pts_in_cluster_i,0])
                intermed_param.v[seq,0] += offset - offset_
                y[pts_in_cluster_i,0] += offset - offset_
            
            # recompute the offset as the x coordinate of
            # rightmost point of the current cluster
            offset = np.max(y[pts_in_cluster_i,0])
    
    def compute_init_embedding(self, d, d_e, Utilde, n_Utilde_Utilde, intermed_param,
                               seq_of_intermed_views_in_cluster,
                               parents_of_intermed_views_in_cluster,
                               C, c, vis, vis_opts, global_opts,
                               print_prop = 0.25):
        M,n = Utilde.shape
        print_freq = int(M*print_prop)

        intermed_param.T = np.tile(np.eye(d),[M,1,1])
        intermed_param.v = np.zeros((M,d))
        y = np.zeros((n,d))

        n_clusters = len(seq_of_intermed_views_in_cluster)
        global_opts['far_off_points'] = compute_far_off_points(d_e, global_opts, force_compute=True)

        # Boolean array to keep track of already visited views
        is_visited_view = np.zeros(M, dtype=bool)
        init_algo = global_opts['init_algo_name']
        self.log('Computing initial embedding using: ' + init_algo + ' algorithm', log_time=True)
        if 'procrustes' == init_algo:
            for i in range(n_clusters):
                # First view global embedding is same as intermediate embedding
                seq = seq_of_intermed_views_in_cluster[i]
                rho = parents_of_intermed_views_in_cluster[i]
                seq_0 = seq[0]
                is_visited_view[seq_0] = True
                y[C[seq_0,:].indices,:] = intermed_param.eval_({'view_index': seq_0,
                                                                'data_mask': C[seq_0,:].indices})
                y, is_visited_view = procrustes_init(seq, rho, y, is_visited_view,
                                            d, Utilde, n_Utilde_Utilde,
                                            C, c, intermed_param,
                                            global_opts, print_freq)
            
            if self.debug:
                self.y_seq_init = y
        
        if 'spectral' == init_algo:
            y_2, y = spectral_alignment(y, d, Utilde,
                                         C, intermed_param, global_opts,
                                         seq_of_intermed_views_in_cluster)
            if self.debug:
                self.y_spec_init = y
                self.y_spec_init_2 = y_2
                
        if 'sdp' == init_algo:
            y_2, y, _ = sdp_alignment(y, d, Utilde,
                                       C, intermed_param, global_opts,
                                       seq_of_intermed_views_in_cluster)
                
        
        self.log('Embedding initialized.', log_time=True)
        self.tracker['init_computed_at'] = time.time()
        if global_opts['compute_error']:
            self.log('Computing error.')
            err = compute_alignment_err(d, Utilde, intermed_param, Utilde.count_nonzero())
            self.log('Alignment error: %0.3f' % (err/Utilde.nnz), log_time=True)
            self.tracker['init_err'] = err
        
        self.add_spacing_bw_clusters(y, d, seq_of_intermed_views_in_cluster,
                                    intermed_param, C)
        
        # Visualize the initial embedding
        color_of_pts_on_tear, y = self.vis_embedding_(y, d, intermed_param, c, C, Utilde,
                                                  n_Utilde_Utilde, global_opts, vis,
                                                  vis_opts, title='Init')
        if self.debug:
            self.intermed_param_init = copy.deepcopy(intermed_param)
        #intermed_param.y = y
        return y, color_of_pts_on_tear

    def compute_Utildeg(self, y, C, global_opts):
        M,n = C.shape
        k_ = min(int(global_opts['k']*global_opts['nu']), n-1)
        neigh_distg, neigh_indg = nearest_neighbors(y, k_, global_opts['metric'])
        Ug = sparse_matrix(neigh_indg,
                           np.ones(neigh_indg.shape,
                                   dtype=bool))

        Utildeg = C.dot(Ug)
        return Utildeg

    def compute_final_embedding(self, y, d, d_e, Utilde, C, c, intermed_param, n_Utilde_Utilde,
                                seq_of_intermed_views_in_cluster,
                                parents_of_intermed_views_in_cluster, 
                                cluster_of_intermed_view, global_opts,
                                vis, vis_opts, reset=True):
        M,n = Utilde.shape
        y = y.copy()
        n_clusters = len(seq_of_intermed_views_in_cluster)
        # Boolean array to keep track of already visited views
        print_freq = int(M*0.25)

        np.random.seed(42) # for reproducbility

        old_time = time.time()
        
        CC = None
        Lpinv_BT = None

        max_iter0 = global_opts['max_iter']
        max_iter1 = global_opts['max_internal_iter']
        refine_algo = global_opts['refine_algo_name']
        patience_ctr = global_opts['patience']
        err_tol = global_opts['err_tol']
        prev_err = None
        Utilde_t = Utilde.copy()
        solver = None
        
        if reset:
            self.y_refined_at = []
            self.tracker['refine_iter_start_at'] = []
            self.tracker['refine_iter_done_at'] = []
            self.tracker['refine_err_at_iter'] = []
            self.tracker['|E(Gamma_t)|'] = []
            self.it0 = 0
            self.refinement_converged = False
        else:
            self.log('Reset is False. Starting from where left off', log_time=True)
            if self.refinement_converged:
                self.log('Refinement had already converged.', log_time=True)
                return self.y_final, self.color_of_pts_on_tear_final
        
        if global_opts['to_tear']:
            Utildeg = self.compute_Utildeg(y, C, global_opts)
        else:
            Utildeg = None
        
        # Refine global embedding y
        for it0 in range(max_iter0):
            self.tracker['refine_iter_start_at'].append(time.time())
            self.log('Refining with ' + refine_algo + ' algorithm for ' + str(max_iter1) + ' iterations.')
            self.log('Refinement iteration: %d' % self.it0, log_time=True)
            
            global_opts['far_off_points'] = compute_far_off_points(d_e, global_opts)
            
            if global_opts['to_tear']:
                Utilde_t = Utildeg.multiply(Utilde)
                Utilde_t.eliminate_zeros()
            
            if refine_algo == 'procrustes':
                y = procrustes_final(y, d, Utilde_t, C, intermed_param, 
                                     seq_of_intermed_views_in_cluster, global_opts)
                    
            elif refine_algo == 'rgd':
                y_2, y = rgd_alignment(y, d, Utilde_t, C, intermed_param, global_opts)
            elif refine_algo == 'gpm':
                y_2, y = gpm_alignment(y, d, Utilde_t, C, intermed_param, global_opts)
            elif refine_algo == 'spectral':
                y_2, y = spectral_alignment(y, d, Utilde_t,
                                             C, intermed_param, global_opts,
                                             seq_of_intermed_views_in_cluster)
            elif refine_algo == 'sdp':
                y_2, y,\
                solver = sdp_alignment(y, d, Utilde_t,
                                       C, intermed_param, global_opts,
                                       seq_of_intermed_views_in_cluster,
                                       solver=solver)
            elif refine_algo == 'ltsa':
                y_2, y = ltsa_alignment(y, d, Utilde_t,
                                         C, intermed_param, global_opts,
                                         seq_of_intermed_views_in_cluster)
                
            self.log('Done.', log_time=True)
            self.tracker['refine_iter_done_at'].append(time.time())

            if global_opts['compute_error'] or (it0 == max_iter0-1):
                self.log('Computing error.')
                err = compute_alignment_err(d, Utilde_t, intermed_param, Utilde.count_nonzero(),
                                            far_off_points=global_opts['far_off_points'],
                                            repel_by=global_opts['repel_by'],
                                            beta=global_opts['beta'])
                self.tracker['refine_err_at_iter'].append(err)
                E_Gamma_t = Utilde_t.nnz
                self.tracker['|E(Gamma_t)|'].append(E_Gamma_t)
                err = err/E_Gamma_t
                self.log('Alignment error: %0.6f' % (err), log_time=True)
                if prev_err is not None:
                    if np.abs(err-prev_err) < err_tol:
                        patience_ctr -= 1
                    else:
                        patience_ctr = global_opts['patience']
                prev_err = err
                
            self.add_spacing_bw_clusters(y, d, seq_of_intermed_views_in_cluster,
                                         intermed_param, C)
            
            # If to tear the closed manifolds
            if global_opts['to_tear']:
                # Compute |Utildeg_{mm'}|
                Utildeg = self.compute_Utildeg(y, C, global_opts)
                color_of_pts_on_tear = self.compute_color_of_pts_on_tear(y, Utilde, C, global_opts,
                                                                         n_Utilde_Utilde,
                                                                         Utildeg)
            else:
                color_of_pts_on_tear = None
                
            if self.debug:
                self.y_refined_at.append(y)
                self.color_of_pts_on_tear_at.append(color_of_pts_on_tear)
            
            #intermed_param.y = y
             
            # Visualize the current embedding
            _, y = self.vis_embedding_(y, d, intermed_param, c, C, Utilde,
                                      n_Utilde_Utilde, global_opts, vis,
                                      vis_opts, title='Iter_%d' % self.it0,
                                      color_of_pts_on_tear=color_of_pts_on_tear,
                                      Utilde_t=Utilde_t)
            
            self.it0 += 1
            if global_opts['compute_error'] and (patience_ctr <= 0):
                self.refinement_converged = True
                break
            
            if (global_opts['repel_by'] is not None):
                global_opts['repel_by'] *= global_opts['repel_decay']
        return y, color_of_pts_on_tear