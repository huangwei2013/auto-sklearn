
from flask import Blueprint,render_template
from flask import request
from demo2.model.model import Model



models = Blueprint('models', __name__)


@models.route('/',methods=['GET', 'POST'])
@models.route('/gets',methods=['GET', 'POST'])
def gets():
    qryresult = Model.query.all()
      
    return render_template('models/index.html', models = qryresult)

@models.route('/get/<int:modelid>', methods = ['GET', 'POST'])
def get(modelid):
    qryresult = Model.query.filter_by(modelid=modelid)
    return render_template('models/index.html', models = qryresult)