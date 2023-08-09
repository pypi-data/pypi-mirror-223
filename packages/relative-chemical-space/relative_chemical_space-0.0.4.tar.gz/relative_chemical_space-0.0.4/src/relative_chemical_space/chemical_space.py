def fragments_compound_space(compounds=None, fragments=None, metric='euclidean', distance_matrix=True, relative_space=False, pca_coordinates=False, input_distance_matrix=None):
    import numpy as np
    from relative_chemical_space.supporting_funtions import distance_space
    from relative_chemical_space.supporting_funtions import non_pca_relative_space
    from relative_chemical_space.supporting_funtions import pca_relative_space
    
    # Distance-based space
        
    if distance_matrix == True and relative_space== False:
        return np.array(distance_space(compounds,fragments,metric))
    
    elif distance_matrix == True and relative_space== True:
        if pca_coordinates == False:
            return np.array(distance_space(compounds,fragments,metric)),np.array(non_pca_relative_space(distance_space(compounds,fragments,metric),metric))
        
        elif pca_coordinates == True and metric.lower() == 'euclidean':
                return np.array(distance_space(compounds,fragments,metric)),np.array(pca_relative_space(fragments,input_distance_matrix))
            
        else:
            raise ValueError("The variable 'pca_coordinates' can only take on the boolean values of True or False.")
            
    elif distance_matrix == False and relative_space== True:
        if pca_coordinates==False:
            return np.array(non_pca_relative_space(input_distance_matrix,metric))
        
        elif pca_coordinates==True and metric.lower() == 'euclidean':
            return np.array(pca_relative_space(fragments,input_distance_matrix))
        
        else:
            raise ValueError("The variable 'pca_coordinates' can only take on the boolean values of True or False.")

