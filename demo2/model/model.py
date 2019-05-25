# -*- coding:utf-8 -*-

from demo2 import db

class Model(db.Model):

    __tablename__ = "t_model"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),unique=True)
    type = db.Column(db.String(10))

    def json(self):
        return self.__dict__
        
    def __rep__(self):
        return '<Model %r>' % (self.name) 

class EnsembelModel(db.Model):

    __tablename__ = "t_ensembel_model"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),unique=True)
    type = db.Column(db.String(20))
    status = db.Column(db.String(20))
    create_time = db.Column(db.String(20))
    finish_time = db.Column(db.String(20))
    ds = db.Column(db.String(20))
    ks = db.Column(db.String(20))
    ensemble_size = db.Column(db.Integer)
    ensemble_rsize = db.Column(db.Integer)
    include_estimators = db.Column(db.Text)
    exclude_estimators = db.Column(db.Text)
    time_left_for_this_task = db.Column(db.Integer)
    per_run_time_limit = db.Column(db.Integer)

    def json(self):
        return self.__dict__
        
    def __rep__(self):
        return '<EnsembelModel %r>' % (self.name) 

class EnsembelSubmodel(db.Model):

    __tablename__ = "t_ensembel_submodel"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.String(20))
    imputation = db.Column(db.String(20))
    weight = db.Column(db.String(10))
    encoding = db.Column(db.String(40))
    estimator = db.Column(db.String(40))
    classifier_params = db.Column(db.Text)
    
    modelid = db.Column(db.Integer, db.ForeignKey('t_model.id'))
    ensembelmodelid = db.Column(db.Integer, db.ForeignKey('t_ensembel_model.id'))
    
    def json(self):
        import json
        dict = self.__dict__
        try:
            dict['classifier_params'] = json.loads(dict['classifier_params'])
        except:
            dict['classifier_params'] = {}
        return dict
        
    def __rep__(self):
        return '<EnsembelSubmodel %r>' % (self.name) 
        
        
if __name__ == '__main__':
    
    ''' 
        test
    '''
    
    import sys
    sys.path.append("..")
    from config import *
    app = create_app()
    
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    
    db.drop_all()
    db.create_all()
    
    model1 = Model(name='模型1', type='classifier')
    model2 = Model(name='模型2', type='classifier')
    model3 = Model(name='模型3', type='regression')
    db.session.add_all([model1, model2, model3])
    db.session.commit()    
    
    ensembelmodel1 = EnsembelModel(name='集成模型1', type='classifier')
    ensembelmodel2 = EnsembelModel(name='集成模型2', type='regression')
    ensembelmodel3 = EnsembelModel(name='集成模型3', type='regression')
    db.session.add_all([ensembelmodel1, ensembelmodel2, ensembelmodel3])
    db.session.commit()    
    
    ensembelSubmodel1 = EnsembelSubmodel(name='集成子模型1', type='classifier', modelid=model1.id, ensembelmodelid=ensembelmodel2.id)
    ensembelSubmodel2 = EnsembelSubmodel(name='集成子模型2', type='regression', modelid=model1.id, ensembelmodelid=ensembelmodel2.id)
    ensembelSubmodel3 = EnsembelSubmodel(name='集成子模型3', type='regression', modelid=model1.id, ensembelmodelid=ensembelmodel2.id)
    db.session.add_all([ensembelSubmodel1, ensembelSubmodel2, ensembelSubmodel3])
    db.session.commit()    
    
    app.debug = True
    app.run(host='0.0.0.0',port=80)
    app.run()    