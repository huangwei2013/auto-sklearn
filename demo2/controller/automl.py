
from flask import Blueprint,render_template
from flask import request
import time
import json

from demo2.model.model import *
from demo2.utils.ensemble import *

automl = Blueprint('automl', __name__)

@automl.route('/ensemble',methods=['GET', 'POST'])
def ensemble(): 
    start_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    
    ensemble_conf = {} # TODO：塞到 create_models() 中
    name = request.form.get('name', default='集成模型-'+ start_time)
    
    pmodel,submodels = create_models()
    
    finish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))    
    ensembelmodel = EnsembelModel(name=name, type='classifier', ds=pmodel['ds'], \
            ks=pmodel['ks'], ensemble_size=pmodel['ensemble_size'], ensemble_rsize=pmodel['ensemble_rsize'], \
            include_estimators = pmodel['include_estimators'], exclude_estimators=pmodel['exclude_estimators'], \
            time_left_for_this_task = pmodel['time_left_for_this_task'], per_run_time_limit = pmodel['per_run_time_limit'], \
            create_time=create_time, finish_time = finish_time, status='done' \
    )
    db.session.add_all([ensembelmodel])
    db.session.commit()    

    ensembelsubmodels = []
    for i in range(len(submodels)):
        newitem = EnsembelSubmodel(name='集成子模型' + str(i), \
            modelid=0, # TODO ： 通过模型名称映射到 modelid
            ensembelmodelid=ensembelmodel.id, \
            weight = submodels[i]['weight'], encoding=submodels[i]['encoding'],imputation=submodels[i]['imputation'], \
            type=submodels[i]['type'], estimator=submodels[i]['estimator'], \
            classifier_params = json.dumps(submodels[i]['classifier_params']) \
        )
        ensembelsubmodels.append(newitem)
    if len(ensembelsubmodels) > 0:
        db.session.add_all(ensembelsubmodels)
        db.session.commit() 
    
    return render_template('automl/ensemble.html',pmodel=pmodel,submodels=submodels)
    
    
@automl.route('/',methods=['GET', 'POST'])
@automl.route('/gets',methods=['GET', 'POST'])
def gets():
    ensembelModels = []
    qryresult = EnsembelModel.query.all()

    return render_template('automl/index.html', models = qryresult)

@automl.route('/get/<int:ensembelmodelid>', methods = ['GET', 'POST'])
def get(ensembelmodelid):
    pmodel = EnsembelModel.query.filter_by(id=ensembelmodelid).first()
    submodels_qryresult = EnsembelSubmodel.query.filter_by(ensembelmodelid=ensembelmodelid)
    submodels = []
    for submodel in submodels_qryresult:
        submodels.append(submodel.json())
    return render_template('automl/ensemble.html',pmodel=pmodel,submodels=submodels)

''' 
    API
'''
@automl.route('/subs/<int:ensembelmodelid>', methods = ['GET', 'POST'])    
def sublist(ensembelmodelid):
    ensembelSubmodels = []
    qryresult = EnsembelSubmodel.query.filter_by(ensembelmodelid=ensembelmodelid)
    return jsonify({"data":qryresult})

