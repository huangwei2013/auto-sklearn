
from flask import Blueprint,render_template
from flask import request

sys = Blueprint('sys', __name__)


@sys.route('/', methods = ['GET', 'POST'])
@sys.route('/index', methods = ['GET', 'POST'])
def info(): 
    
    return render_template('sys/info.html')
    
