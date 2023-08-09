#!/usr/bin/env python
# coding: utf-8

# In[1]:


def distance_space(compounds,fragments,metric):
    from scipy.spatial import distance 
    from master_strange_mol_rep import mol_rep as strange # For arrays manipulation
    if compounds.shape[1] > fragments.shape[1]:
        fragments=strange.zero_pad_two_ndarrays(compounds,fragments)
    else:
        compounds=strange.zero_pad_two_ndarrays(fragments,compounds)
    
    
    total_similarity=[]
    for i in compounds:
        similarity=[]
        for u in fragments:
            if metric.lower() == 'euclidean':
                similarity.append(distance.euclidean(u,i))
            elif metric.lower() == 'cosine':
                similarity.append(distance.cosine(u,i))
            elif metric.lower() == 'canberra':
                similarity.append(distance.canberra(u,i))
            elif metric.lower() == 'manhattan':
                similarity.append(distance.cityblock(u,i))
            else:
                raise ValueError("Please choose between the Euclidean, Cosine, Canberra, and Manhattan distance metrics.")
        total_similarity.append(similarity)
    return total_similarity


# In[2]:


def non_pca_relative_space(total_similarity,metric):
    import numpy as np
    import pandas as pd
    
    relative_rep=[]
    rep_cs=np.array(total_similarity)
    bb_a=np.zeros((rep_cs.shape[1],rep_cs.shape[1]))
    bb_a[np.diag_indices_from(bb_a)] = 1
    if metric.lower() == 'euclidean':
        asd=[]
        bb_array=pd.DataFrame(bb_a)
        for i in range(bb_a.shape[0]):
            asd.append((bb_a[0]-bb_a[i])*-2)
        asd.append((bb_a[1]-bb_a[2])*-2)
                  
        bb_mat=pd.DataFrame(asd)
        rep=pd.DataFrame(rep_cs)

        for i in range(rep.shape[0]):
            A = np.array(pd.DataFrame(np.array(bb_mat)))
            b = np.array(rep.iloc[i])
        
            qas=[]
            for t in range(len(b)):
                qas.append(b[0]**2-b[t]**2)
            qas.append(b[1]**2-b[2]**2)
        
            x=np.linalg.solve(A[1:]+0.001,qas[1:])
            relative_rep.append(x)    
    
    elif metric.lower() == 'canberra':
        asdf=[]
        bb_array=pd.DataFrame(bb_a)
        dist=rep.iloc[i]
        A=np.array(bb_array*(dist-4))
        b=2-dist
        for t in np.linalg.solve(A,pd.DataFrame(b)):
            asdf.append(float(t))
        relative_rep.append(asdf)
    else:
        raise ValueError("The generation of the non-PCA relative space is restricted to the utilisation of the Euclidean and Canberra distance-based spaces exclusively.")
    return relative_rep


# In[3]:


def pca_relative_space(fragments,input_distance_matrix):
    import numpy as np
    import pandas as pd
    from sklearn.decomposition import PCA # Necessary for the creation of the PCA-based space
    
    A=fragments
    pca = PCA(n_components=A.shape[0])
    Y=pca.fit_transform(A)
    bbb=[]
    for i in range(0,Y.shape[1],1):
        aaa=[]
        for u in range(0,Y.shape[0],1):
            aaa.append(Y[0][i]-Y[u][i])
        aaa.append(Y[1][i]-Y[2][i])
        bbb.append(aaa)
    E=pd.DataFrame(Y*Y)*-1
    B=pd.DataFrame(input_distance_matrix)
    C=B*B
    aza1=[]
    for u in range(0,C.shape[0],1):
        aza=[]
        for q in range(0,C.shape[1],1):
            aza.append(C.iloc[u][0]-C.iloc[u][q]+sum(E.iloc[0])-sum(E.iloc[q]))
        aza.append(C.iloc[u][1]-C.iloc[u][2]+sum(E.iloc[1])-sum(E.iloc[2]))
        aza1.append(aza)
    qwe=[]
    for i in aza1:
        qwe.append(np.linalg.solve(np.array(0.0001+pd.DataFrame(bbb).T[1:])*-2,i[1:]))
    return qwe

