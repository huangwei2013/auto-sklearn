# auto-sklearn

Some codes, FAQ when exploring auto-sklearn.


## Environment：

### install

```
// Dependecy
curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip3 install
        
//auto-sklearn
pip3 install auto-sklearn

(pyrfr installed by pip3，needs memory >= 600MB)    
```

### Server
1C1G (Yes, Poor Cloud VirtualMachine from AliCloud) <br/>
Centos 7.5 (3.10.0-862.14.4.el7.x86_64) <br/>
   
### Software
* python 3.6.1 
* sklearn 0.19.2
* auto-sklearn 0.5.1
  
## Demos：

* Demo1
  Get information from ensembled models（KS、AUC、submodels' attributes，etc），display on page（by jinja2）

* Demo2
  Better project structure based on demo1
  More function for data storage 
