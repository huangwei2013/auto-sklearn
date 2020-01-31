
## Q：Runtime Error
    ValueError: Cannot load file containing pickled data when allow_pickle=False
## A：
```
    2019.01 
      Numpy Securty Report(1.10-1.6.x)
      fixed >=1.16.3 ,by changed the initial input params, while autosklearn may keep as before
    
    avoided by :
      numpy/lib/npyio.py
        revised:  
          allow_pickle=False
        to:
          allow_pickle=True
```

或中文版：
```
    (2019.01 Numpy 报出安全漏洞，影响版本 1.10-1.16.x，至少1.16.3 起修改了初值设置，可能autosklearn版本没有对应修改设置，因此报错)
    将对应库 numpy/lib/npyio.py
    中的  
        allow_pickle=False
    改成
         allow_pickle=True
```

## Q：获取生成模型的内部参数
## A：
```
    print(automl.show_models()) #在这个之后，使用以下代码

    models_with_weights = automl.get_models_with_weights()
    for weight, model in models_with_weights:
        print(weight)
        print(model)
        print(dir(model))
        print(model.__dict__)
        print(model.__dict__['dataset_properties_']['target_type']]) # 重要，很多信息来自于这种格式的取值
        print(model.configuration['classifier:__choice__']) #同上
        print(model.configuration['categorical_encoding:__choice__']) #同上
        steps = model._get_pipeline()
        for sname,sobj in steps:
             print(sname)
             print(sobj.__dict__)
```

## Q：代码块-解析automl内容
## A：
```
def getClassiferParams(classifier, dict_params):
    
    //    获取不同算法的主要指标&值    
    //    @input classifier [string] 算法名称
    //    @input dict_params [dict]  生成模型的参数，来自 automl.get_models_with_weights() 的 model.configuration    

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
    }
    
    params = {}
    if classifier in dict_param_configs:
        prefix = 'classifier:' + classifier + ':'
            
        for idx, val in dict_param_configs[classifier].items():         
            key = prefix + idx
            try:
                if val != '':
                    params[val] = dict_params[key]
                else:
                    params[idx] = dict_params[key]
            except Exception(e):
                print(' %s works not good : %s', (classifier, key, repr(e)))

    return params
```
