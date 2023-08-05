# -*- coding: utf-8 -*-
"""
@author: Antoine Guillaume
"""
from numpy.random import choice, uniform, random, seed
from numpy import (
    unique, where, percentile, int64, bool_, float64, concatenate,
    dot, log2, floor_divide, zeros, floor, power, ones, cumsum, mean, std,
    arange
)

from convst.transformers._commons import (
    get_subsequence, compute_shapelet_dist_vector,
    apply_one_shapelet_one_sample_multivariate, _combinations_1d,
    generate_strides_2D, prime_up_to, choice_log
)

from numba import njit, prange

from convst import (
    __USE_NUMBA_CACHE__, __USE_NUMBA_FASTMATH__,
    __USE_NUMBA_NOGIL__, __USE_NUMBA_PARALLEL__
)


@njit(cache=__USE_NUMBA_CACHE__, nogil=__USE_NUMBA_NOGIL__)
def M_SL_init_random_shapelet_params(
    n_shapelets, shapelet_sizes, n_timestamps, p_norm, max_channels, prime_scheme
):
    """
    Initialize the parameters of the shapelets.    

    Parameters
    ----------
    n_shapelets : int
        Number of shapelet to initialize
    shapelet_sizes : array, shape=()
        Set of possible length for the shapelets
    n_timestamps : int
        Number of timestamps in the input data
    p_norm : float
        A value in the range [0,1] indicating the chance for each
        shapelet to use z-normalized distance
    max_channels : int
        The maximum number of features considered for one shapelet
    prime_scheme : bool
        Wheter to only consider prime numbers as possible dilation 

        
    Returns
    -------
    values : array, shape=(n_shapelet, max(shapelet_sizes))
        An initialized (empty) value array for each shapelet
    lengths : array, shape=(n_shapelet)
        The randomly initialized length of each shapelet
    dilations : array, shape=(n_shapelet)
        The randomly initialized dilation of each shapelet
    threshold : array, shape=(n_shapelet)
        An initialized (empty) value array for each shapelet
    normalize : array, shape=(n_shapelet)
        The randomly initialized normalization indicator of each shapelet
    channels : array, shape=(n_shapelet, n_features)
        The features considered by each shapelet
    """
    # Lengths of the shapelets
    lengths = choice(shapelet_sizes, size=n_shapelets).astype(int64)

    # Dilations
    upper_bounds = log2(floor_divide(n_timestamps - 1, lengths - 1))
    if prime_scheme:
        primes = prime_up_to(int64(2**upper_bounds.max()))
        dilations = zeros(n_shapelets, dtype=int64)
        #TODO : optimize to avoid recomputing choice log for all upper bounds
        #Loop on each unique upper bounds ?
        for i in prange(n_shapelets):
            shp_primes = primes[primes<=int64(2**upper_bounds[i])]
            dilations[i] = shp_primes[choice_log(shp_primes.shape[0], 1)[0]]
    else:
        powers = zeros(n_shapelets)
        for i in prange(n_shapelets):
            powers[i] = uniform(0, upper_bounds[i])
        dilations = floor(power(2, powers)).astype(int64)
    
    # Init threshold array
    threshold = zeros(n_shapelets)

    # channels (i.e. features)
    n_channels = choice(max_channels, size=n_shapelets)+1

    channel_ids = zeros(n_channels.sum(), dtype=int64)

    # Init values array
    values = zeros(
        int64(
            dot(lengths.astype(float64), n_channels.astype(float64))
        )
    )

    # Is shapelet using z-normalization ?
    normalize = random(size=n_shapelets)
    normalize = (normalize < p_norm)

    return values, lengths, dilations, threshold, normalize, n_channels, channel_ids

@njit(cache=__USE_NUMBA_CACHE__, parallel=__USE_NUMBA_PARALLEL__, nogil=__USE_NUMBA_NOGIL__)
def M_SL_generate_shapelet(
    X, y, n_shapelets, shapelet_sizes, r_seed, p_norm, p_min, p_max, alpha,
    use_phase, max_channels, prime_scheme
):
    """
    Given a time series dataset and parameters of the method, generate the
    set of random shapelet that will be used in the rest of the algorithm.

    Parameters
    ----------
    X : array, shape=(n_samples, n_features, n_timestamps)
        Time series dataset
    y : array, shape=(n_samples)
        Class of each input time series
    n_shapelets : int
        Number of shapelet to generate
    shapelet_sizes : array, shape=()
        An array of possible shapelet length.
    seed : int
        Random seed generator for numpy
    p_norm : float
        Probability of each shapelet to use z-normalized distance
    p_min : float
        Lower bound for the percentile during the choice of threshold
    p_max : float
        Upper bound for the percentile during the choice of threshold
    alpha : float
        Alpha similarity parameter
    use_phase: bool
        Wheter to use phase invariance
    prime_scheme : bool
        Wheter to only consider prime numbers as possible dilation 

    
    Returns
    -------
    set of array, shape=(5)
        values : array, shape=(n_shapelets, max(shapelet_sizes))
            Values of the shapelets. If the shapelet use z-normalized distance,
            those values are already z-normalized by the shapelet 
            initialization step.
        lengths : array, shape=(n_shapelets)
            Length parameter of the shapelets
        dilations : array, shape=(n_shapelets)
            Dilation parameter of the shapelets
        threshold : array, shape=(n_shapelets)
            Threshold parameter of the shapelets
        normalize : array, shape=(n_shapelets)
            Normalization indicator of the shapelets
    """
    n_samples, n_features, n_timestamps = X.shape
    # Fix the random seed
    seed(r_seed)

    #Initialize shapelets
    values, lengths, dilations, threshold, normalize, n_channels, channel_ids = \
    M_SL_init_random_shapelet_params(
        n_shapelets, shapelet_sizes, n_timestamps, p_norm, max_channels, prime_scheme
    )
    #Initialize self similarity mask
    unique_dil = unique(dilations)
    mask_sampling = ones(
        (2,unique_dil.shape[0],n_samples,n_features,n_timestamps), dtype=bool_
    )
    mask_return = ones(n_shapelets, dtype=bool_)
    #values[idx_val[i]:idx_val[i+1]]=_val
    a1 = concatenate((zeros(1, dtype=int64),cumsum(n_channels*lengths)))
    #same for channels
    a2 = concatenate((zeros(1, dtype=int64),cumsum(n_channels)))   

    #For each dilation, we can do in parallel
    for i_d in prange(unique_dil.shape[0]):
        #For each shapelet id with this dilation
        id_shps = where(dilations==unique_dil[i_d])[0]
        min_l = min(lengths[id_shps])
        for i_shp in id_shps:
            _dilation = dilations[i_shp]
            _length = lengths[i_shp]
            norm = int64(normalize[i_shp])
            _n_channels = n_channels[i_shp]
            if use_phase:
                d_shape = n_timestamps
            else:
                d_shape = n_timestamps-(_length-1)*_dilation
            mask_dil = mask_sampling[norm,i_d]
            
            #Possible sampling points given self similarity mask
            
            _values = zeros(_n_channels * _length)
            
            _channel_ids = choice(
                arange(0, n_features), _n_channels, replace=False
            )
            
            i_mask = where(
                mask_dil[:,_channel_ids,:d_shape].sum(axis=1)>=_n_channels*alpha
            )
            
            if i_mask[0].shape[0] > 0:
                x_dist = zeros(d_shape)
                #Choose a sample
                id_sample = choice(i_mask[0])
                #Choose a timestamp
                index = choice(i_mask[1][i_mask[0]==id_sample])
                #Counter to keep track of indexes for value affectation
                a3 = 0
                
                #Select another sample of the same class as the sample used
                loc_others = where(y == y[id_sample])[0]
                if loc_others.shape[0] > 1:
                    loc_others = loc_others[loc_others != id_sample]
                    id_test = choice(loc_others)
                else:
                    id_test = id_sample
                
                #Update the mask
                alpha_size = _length - int64(max(1,(1-alpha)*min_l))
                for k in range(_n_channels):
                    for j in range(alpha_size):
                        #We can use modulo even without phase invariance, as we
                        #limit the sampling to d_shape
                        mask_sampling[
                            norm, i_d, id_sample, _channel_ids[k],
                            (index-(j*_dilation))%n_timestamps
                        ] = False
                        mask_sampling[
                            norm, i_d, id_sample, _channel_ids[k],
                            (index+(j*_dilation))%n_timestamps
                        ] = False
                    
                    b3 = a3 + _length
                    #Extract the values
                    _v = get_subsequence(
                        X[id_sample, _channel_ids[k]], index, _length,
                        _dilation, norm, use_phase
                    )
                    
                    #Compute distance vector
                    x_dist += compute_shapelet_dist_vector(
                        X[id_test, _channel_ids[k]], _v, _length, _dilation,
                        norm, use_phase
                    )
                    
                    _values[a3:b3] = _v
                    a3 = b3
                
                values[a1[i_shp]:a1[i_shp+1]] = _values
                channel_ids[a2[i_shp]:a2[i_shp+1]] = _channel_ids
                
                #Extract value between two percentile as threshold for SO
                ps = percentile(x_dist, [p_min,p_max])
                threshold[i_shp] = uniform(
                    ps[0], ps[1]
                )
            else:
                mask_return[i_shp] = False
            
    lengths = lengths[mask_return]
    n_channels = n_channels[mask_return]
    mask_channel_ids = zeros(n_channels.sum(), dtype=int64)
    mask_values = zeros(
        int64(
            dot(lengths.astype(float64), n_channels.astype(float64))
        )
    )
    
    c1 = 0
    c2 = 0
    for idx, i_shp in enumerate(where(mask_return)[0]):        
        d1 = c1 + (n_channels[idx] * lengths[idx])
        d2 = c2 + n_channels[idx]
        
        mask_values[c1:d1] = values[a1[i_shp]:a1[i_shp+1]]
        mask_channel_ids[c2:d2] = channel_ids[a2[i_shp]:a2[i_shp+1]]
        
        c1 = d1
        c2 = d2
    
    return (
        mask_values,
        lengths,
        dilations[mask_return],
        threshold[mask_return],
        normalize[mask_return],
        n_channels,
        mask_channel_ids
    )

@njit(cache=__USE_NUMBA_CACHE__, parallel=__USE_NUMBA_PARALLEL__, fastmath=__USE_NUMBA_FASTMATH__, nogil=__USE_NUMBA_NOGIL__)
def M_SL_apply_all_shapelets(
    X, shapelets, use_phase
):
    """
    Apply a set of generated shapelet using the parameter arrays previously 
    generated to a set of time series.

    Parameters
    ----------
    X : array, shape=(n_samples, n_features, n_timestamps)
        Input time series
    shapelets: set of array, shape=(5)
        values : array, shape=(n_shapelets, max(shapelet_sizes))
            Values of the shapelets. If the shapelet use z-normalized distance,
            those values are already z-normalized by the shapelet 
            initialization step.
        lengths : array, shape=(n_shapelets)
            Length parameter of the shapelets
        dilations : array, shape=(n_shapelets)
            Dilation parameter of the shapelets
        threshold : array, shape=(n_shapelets)
            Threshold parameter of the shapelets
        normalize : array, shape=(n_shapelets)
            Normalization indicator of the shapelets
    use_phase: bool
        Wheter to use phase invariance
    
    Returns
    -------
    X_new : array, shape=(n_samples, 3*n_shapelets)
        The transformed input time series with each shapelet extracting 3
        feature from the distance vector computed on each time series.

    """
    (values, lengths, dilations, threshold, 
     normalize, n_channels, channel_ids) = shapelets
    n_shapelets = len(lengths)
    n_samples, n_ft, n_timestamps = X.shape
    n_features = 3
    
    #(u_l * u_d , 2)
    params_shp = _combinations_1d(lengths, dilations)
    #(u_l * u_d) + 1
    n_shp_params = zeros(params_shp.shape[0]+1, dtype=int64)
    #(n_shapelets)
    idx_shp = zeros(n_shapelets, dtype=int64)
    
    #Indexes per shapelets for values array
    a1 = concatenate((zeros(1, dtype=int64),cumsum(n_channels*lengths)))
    #Indexes per shapelets for channel_ids array
    a2 = concatenate((zeros(1, dtype=int64),cumsum(n_channels)))
    # Counter for shapelet params array
    a3 = 0
    
    for i in range(params_shp.shape[0]):
        _length = params_shp[i, 0]
        _dilation = params_shp[i, 1]
        
        ix_shapelets = where((lengths == _length) & (dilations == _dilation))[0]
        b = a3 + ix_shapelets.shape[0]
        
        idx_shp[a3:b] = ix_shapelets
        n_shp_params[i+1] = ix_shapelets.shape[0]
        
        a3 = b
    n_shp_params = cumsum(n_shp_params)
    
    X_new = zeros((n_samples, n_features * n_shapelets))
    for i_sample in prange(n_samples):
        #n_shp_params is a cumsum starting at 0
        for i_shp_param in prange(n_shp_params.shape[0]-1):
            _length = params_shp[i_shp_param, 0]
            _dilation = params_shp[i_shp_param, 1]
            
            strides = generate_strides_2D(
                X[i_sample], _length, _dilation, use_phase
            )
            # Indexes of shapelets corresponding to the params of i_shp_param
            _idx_shp = idx_shp[n_shp_params[i_shp_param]:n_shp_params[i_shp_param+1]]
            
            _idx_no_norm = _idx_shp[where(normalize[_idx_shp] == False)[0]]
            for i_idx in range(_idx_no_norm.shape[0]):               
                i_shp = _idx_no_norm[i_idx]
                _channels = channel_ids[a2[i_shp]:a2[i_shp+1]]
                _values = values[a1[i_shp]:a1[i_shp+1]].reshape(
                    n_channels[i_shp], _length
                )

                X_new[i_sample, (n_features * i_shp):(n_features * i_shp + n_features)] = \
                apply_one_shapelet_one_sample_multivariate(
                    strides[_channels], _values, threshold[i_shp]
                )
                        
            _idx_norm = _idx_shp[where(normalize[_idx_shp] == True)[0]]
            if _idx_norm.shape[0] > 0:
                #n_features
                for i_stride in range(strides.shape[0]):
                    #n_timestamps
                    for j_stride in range(strides.shape[1]):
                      _str = strides[i_stride,j_stride]
                      strides[i_stride,j_stride] = (_str - mean(_str))/(std(_str)+1e-8)
                          
                for i_idx in range(_idx_norm.shape[0]):               
                    i_shp = _idx_norm[i_idx]
                    _channels = channel_ids[a2[i_shp]:a2[i_shp+1]]
                    _values = values[a1[i_shp]:a1[i_shp+1]].reshape(
                        n_channels[i_shp], _length
                    )
                    
                    X_new[i_sample, (n_features * i_shp):(n_features * i_shp + n_features)] = \
                    apply_one_shapelet_one_sample_multivariate(
                        strides[_channels], _values, threshold[i_shp]
                    )
    return X_new