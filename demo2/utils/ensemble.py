#encoding=utf8


import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
import autosklearn.classification


def getClassiferParams(classifier, dict_params):
    '''
        获取不同算法的主要指标&值
        
        @input classifier [string] 算法名称
        @input dict_params [dict]  生成模型的参数，来自 automl.get_models_with_weights() 的 model.configuration
        
    '''
    
    dict_param_configs = {
        'lda' : {
            'n_components':'维数', #LDA降维时降到的维数。在降维时需要输入这个参数。注意只能为[1,类别数-1)范围之间的整数
            'shrinkage':'正则化参数', #增强LDA分类的泛化能力
            'tol':'',
        },
        'xgradient_boosting' : {
            'base_score':'',
            'booster':'',
            'colsample_bylevel':'',
            'colsample_bytree':'',
            'gamma':'',
            'learning_rate':'',
            'max_delta_step':'',
            'max_depth':'',
            'min_child_weight':'',
            'n_estimators':'',
            'reg_alpha':'',
            'reg_lambda':'',
            'scale_pos_weight':'',
            'subsample':'',
        },
        'libsvm_svc' : {
            'C':'',
            'coef0':'',
            'degree':'',
            'gamma':'',
            'kernel':'',
            'max_iter':'',
            'mashrinkingx_iter':'',
            'tol':'',
        }, 
        'extra_trees' : {
            'bootstrap':'',
            'criterion':'',
            'max_depth':'',
            'max_features':'',
            'max_leaf_nodes':'',
            'min_impurity_decrease':'',
            'min_samples_leaf':'',
            'min_samples_split':'',
            'min_weight_fraction_leaf':'',
            'n_estimators':'',
        },     
        'gradient_boosting' : {
            'criterion':'',
            'learning_rate':'',
            'loss':'',
            'max_depth':'',
            'max_features':'',
            'max_leaf_nodes':'',
            'min_impurity_decrease':'',
            'min_samples_leaf':'',
            'min_samples_split':'',
            'min_weight_fraction_leaf':'',
            'n_estimators':'',
            'subsample':'',
        },    
        'adaboost' : {
            'algorithm':'',
            'learning_rate':'',
            'max_depth':'',
            'n_estimators':'',
        },
        'passive_aggressive' : {
            'C':'',
            'average':'',
            'fit_intercept':'',
            'loss':'',
            'tol':'',
        },  
        'liblinear_svc_preprocessor' : {
            'C':'',
            'dual':'',
            'fit_intercept':'',
            'intercept_scaling':'',
            'loss':'',
            'multi_class':'',
            'penalty':'',
            'tol':'',
        },   
        'liblinear_svc' : {
            'C':'',
            'dual':'',
            'fit_intercept':'',
            'intercept_scaling':'',
            'loss':'',
            'multi_class':'',
            'penalty':'',
            'tol':'',
        },
        'k_nearest_neighbors' : {
            'n_neighbors':'',
            'p':'',
            'weights':'',
        }, 
        'polynomial' : {
            'degree':'',
            'include_bias':'',
            'interaction_only':'',
        },   
        'sgd' : {
            'alpha':'',
            'average':'',
            'eta0':'',
            'fit_intercept':'',
            'learning_rate':'',
            'loss':'',
            'penalty':'',
            'power_t':'',
            'tol':'',
        },       
        'random_forest' : {
             'bootstrap':'',
             'criterion':'',
             'max_depth':'',
             'max_features':'',
             'max_leaf_nodes':'',
             'min_impurity_decrease':'',
             'min_samples_leaf':'',
             'min_samples_split':'',
             'min_weight_fraction_leaf':'',
             'n_estimators':'',
        },
        'bernoulli_nb' : {
            'alpha':'',
            'fit_prior':'',
        },           
    } 
  
    params = {}
    print(dict_params)
    for idx, val in dict_param_configs[classifier].items():  
        '''
            TODO：抽取的属性值还可以更多一些
        '''
        prefix = 'classifier:' + classifier + ':'
            
        for idx, val in dict_param_configs[classifier].items():  
            key = prefix + idx
            
            try:
                if val != '':
                    params[val] = dict_params[key]
                else:
                    params[idx] = dict_params[key]
            except Exception(e):
                print(' %s works not good : %s', (classifier,key, repr(e)))

    return params
    

def create_models():
    testdata = sklearn.datasets.load_breast_cancer()

    X = testdata.data
    y = testdata.target
    X_train, X_test, y_train, y_test = \
        sklearn.model_selection.train_test_split(X, y, test_size=.3, random_state=1)

    time_left_for_this_task = 60
    per_run_time_limit = 60
    include_estimators = None # ["xgradient_boosting", "lda" ]
    exclude_estimators = None
    ensemble_size = 4
    automl = autosklearn.classification.AutoSklearnClassifier(
        time_left_for_this_task=time_left_for_this_task, per_run_time_limit=per_run_time_limit,
        include_estimators=include_estimators, exclude_estimators=exclude_estimators,
        ensemble_size=4,
        tmp_folder='/tmp/autoslearn_classification_example_tmp',
        output_folder='/tmp/autosklearn_classification_example_out')
    automl.fit(X_train, y_train)
    y_pred = automl.predict(X_test)

    testdata.name = 'breast_cancer'
    pmodel = {
        'ds': testdata.name,
        'ensemble_rsize':0,
        'ks':0,
        'time_left_for_this_task':per_run_time_limit,
        'per_run_time_limit':per_run_time_limit,
        'include_estimators':include_estimators,
        'exclude_estimators':exclude_estimators,
        'ensemble_size':ensemble_size, 
    }
    submodels = []
    
    from scipy.stats import ks_2samp
    get_ks = lambda y_pred,y_test: ks_2samp(y_pred[y_test==1], y_pred[y_test!=1]).statistic
    pmodel['ks'] = get_ks(automl.predict_proba(X_test)[:,0], y_test)
    
    from sklearn.metrics import roc_auc_score
    pmodel['auc'] = roc_auc_score(y_test,y_pred)    

    submodels_with_weights = automl.get_models_with_weights()
    for weight, submodel in submodels_with_weights:
        pmodel['ensemble_rsize'] = pmodel['ensemble_rsize'] + 1

        list_classifier_params = []
        dict_params = getClassiferParams(submodel.configuration['classifier:__choice__'], submodel.configuration)
        for (k,v) in dict_params.items():
            list_classifier_params.append(k+" : "+str(v))

        item = {
            'ensemble_rsize' : pmodel['ensemble_rsize'],
            'weight' : weight,
            'type' : submodel.__dict__['dataset_properties_']['target_type'],
            'estimator' : submodel.configuration['classifier:__choice__'],
            'encoding' : submodel.configuration['categorical_encoding:__choice__'],
            'imputation' : submodel.configuration['imputation:strategy'],
            'classifier_params' : list_classifier_params
        }
        submodels.append(item)
        
    return pmodel,submodels