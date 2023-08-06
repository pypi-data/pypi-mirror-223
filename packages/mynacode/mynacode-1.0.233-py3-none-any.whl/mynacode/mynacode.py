import numpy as np
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil
from datetime import datetime
from sklearn import metrics
import matplotlib.pyplot as plt
import dill
import urllib.request
from pathlib import Path
import glob
import shutil, yaml

#protocol = 'http'
protocol = 'https'

#IP = '127.0.0.1:8000'
IP = 'mynacode.com'

username = ""
key = ""
run_id_global = ""
project_id_global = ""
run_dir_global = ""
project_dir_global = ""
prev_max = -9999999999
prev_min = 9999999999
metric_values = []
metric_index = 0
index_count = 0
  

def login(uname, ky):
  global username
  global key
  
  print("Logging in...")
  credentials = {'username':uname, 'key':ky, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)
  
  if response.text == '1':
    username = uname
    key = ky
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")


def metadata(run_id):

  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  system_info_list = ['Codebase Python ' + platform.python_version()]
  
  system_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          system_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            system_info_list.append("GPU ID " + str(gpu_id))
            system_info_list.append(gpu_name)
            system_info_list.append(str(gpu_memory) + " MB")
  except:
      system_info_list.append("No NVIDIA Driver found")

  system_info_list.append("    CPU    ")
  system_info_list.append(platform.processor())
  system_info_list.append(platform.platform())
  system_info_list.append(platform.machine())
  system_info_list.append("    MEMORY    ")
  system_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'run_id' : run_id, 'installed_packages': str(installed_packages_list), 'username': username, 'key': key, 'system_information': str(system_info_list)}
  
  response = requests.post(protocol+'://'+IP+'/api/add_metadata', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    print("Metadata saved")


def create_project(project_name = ""):
    data = {'project_name': project_name, 'username': username, 'key': key}
    response = requests.post(protocol+'://'+IP+'/api/create_project_python', data=data)

    return response.text


def create_run(project_id = None):
    if not project_id:
      print("Please provide project ID")
      return
    
    data = {'project_id': project_id, 'username': username, 'key': key}
    response = requests.post(protocol+'://'+IP+'/api/create_run_python', data=data)

    return response.text


def start(base_folder = "", project_name = "", save_files = False):
    global project_id_global
    global run_id_global
    global run_dir_global
    global project_dir_global
    global prev_max 
    global prev_min
    global metric_values
    global metric_index
    global index_count

    prev_max = -9999999999
    prev_min = 9999999999
    metric_values = []
    metric_index = 0
    index_count = 0
    
    if len(base_folder) == 0:
      print("Using current working directory")
      base_folder = Path.cwd().as_posix()
    elif not os.path.exists(base_folder):
      print("Using current working directory. Path not found: ", base_folder)
      base_folder = Path.cwd().as_posix()

    if not os.path.exists(base_folder+'/'+'mynacode'):
      os.mkdir(base_folder+'/mynacode')

    if len(project_name) == 0:
      project_name = 'myna_project'

    if not os.path.exists(base_folder+'/mynacode/'+project_name):
      os.mkdir(base_folder+'/mynacode/'+project_name)

    p_id = create_project(project_name)
    r_id = create_run(int(p_id))

    project_id_global = p_id
    run_id_global = r_id
    project_dir_global = base_folder+'/mynacode/'+project_name
    run_dir_global = base_folder+'/mynacode/'+project_name+'/'+str(r_id)+'_'+str(datetime.now())[:10]

    os.mkdir(run_dir_global)

    if save_files == True:
      py_files = glob.glob('./**/*.py', recursive=True)
      ipynb_files = glob.glob('./**/*.ipynb', recursive=True)

      if not os.path.exists(run_dir_global+'/files/'):
        os.mkdir(run_dir_global+'/files/')

      for file in py_files:
        shutil.copy(file, run_dir_global+'/files/')

      for file in ipynb_files:
        shutil.copy(file, run_dir_global+'/files/')

      data = {'run_id' : run_id_global, 'config_dict': str({"python_files":run_dir_global+'/files/'}), 'node_name': "Datasets", 'username': username, 'key': key}

      response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)
    

  

def csv(run_id, dataframe, node_name="CSV"):
    columns_list = dataframe.columns.values.tolist()
    isnull_list = dataframe.isnull().sum().values.tolist()
    isunique_list = dataframe.nunique().values.tolist()
    size = sys.getsizeof(dataframe)/1024
    shape = dataframe.shape
    dtypes_list = []

    for d in dataframe.dtypes:
        dtypes_list.append(str(d))

    data = {'run_id': run_id, 'columns_list': str(columns_list), 'isnull_list': str(isnull_list),
            'isunique_list': str(isunique_list), 'dtypes_list': str(dtypes_list),
            'username': username, 'size': int(size), 'shape': str(shape), 'key': key, 'node_name': node_name}

    response = requests.post(protocol+'://'+IP+'/api/add_csv', data=data)

    if response.text == '0':
      print("Authentication failed")
    else:
      print("CSV Information saved.")  

    

def specificity(y_true, y_pred):
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_truth = np.count_nonzero(y_true == 0)
   
    return float(y_correct/y_truth)

def npv(y_true, y_pred): #Negative Predicted Value
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_predicted = np.count_nonzero(y_pred == 0)
   
    return float(y_correct/y_predicted)

def get_roc_auc(y_true, y_pred):
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_pred)
    roc_auc = metrics.auc(fpr, tpr)
    gmeans = np.sqrt(tpr * (1 - fpr)) #sensitivity * specificity (element-wise)
    index = np.argmax(gmeans) #Returns index of max value
    best_threshold = threshold[index]
   
    return fpr, tpr, roc_auc, gmeans, best_threshold, index

def get_metrics(y_true, y_pred, threshold):
    y_pred_binary = (y_pred > threshold).astype('float')
   
    prec = metrics.precision_score(y_true, y_pred_binary)
    rec = metrics.recall_score(y_true, y_pred_binary)
    spec = specificity(y_true, y_pred_binary)
    f1 = metrics.f1_score(y_true, y_pred_binary)
    acc = metrics.accuracy_score(y_true, y_pred_binary)
    npv_val = npv(y_true, y_pred_binary)
   
    c_matrix = metrics.confusion_matrix(y_true, y_pred_binary, labels=[0,1])

    c_matrix = c_matrix.tolist()

    c_matrix = [item for sublist in c_matrix for item in sublist]
   
    return prec, rec, spec, f1, acc, npv_val, c_matrix


def results(run_id, y_true = [], y_predicted = [], threshold=0.5, results_dict = {}, node_name="Results", problem_type = 'binary classification'):

    if not run_id:
      run_id = run_id_global
    
    if len(y_true) != 0 and len(y_predicted) != 0:
      
      y_predicted = np.array(y_predicted).flatten()
      y_true = np.array(y_true).flatten()

      zero_idx = np.where(y_true == 0)[0]
      one_idx = np.where(y_true == 1)[0]
      
      prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_predicted, threshold)
      fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_predicted)


      #pred_hist = plt.hist(y_predicted, bins=hist_bins)
      #freq = pred_hist[0]
      #bins = pred_hist[1]
      #'freq': freq.tolist(), 'bins': bins.tolist()

      binary = {'precision': round(prec, 4), 'recall': round(rec, 4), 'specificity': round(spec, 4),
              'f1': round(f1, 4), 'accuracy': round(acc, 4), 'npv': round(npv_val, 4), 'c_matrix': c_matrix,
              'test_auc': roc_auc, 'zero_prob': y_predicted[zero_idx].tolist(), 'one_prob': y_predicted[one_idx].tolist(),
                'fpr': fpr.tolist(), 'tpr': tpr.tolist(), 'threshold': round(threshold, 4)}

      results_dict.update(binary)

    data = {'run_id' : run_id, 'results_dict': str(results_dict), 'node_name': node_name, 'username': username, 'key': key}

    response = requests.post(protocol+'://'+IP+'/api/add_results', data=data)
  
    if response.text == '0':
      print("Authentication failed")
    else:
      print("Results saved")



def save_torch_model(run_id, model):
    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')
      
    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'wb') as f:
        dill.dump(model, f)

    torch.save(model.state_dict(), 'mynacode/'+str(run_id)+'/saved_state_dict.pt')
        
    files = {'network': open('mynacode/'+str(run_id)+'/saved_network.pkl','rb'), 'state_dict': open('mynacode/'+str(run_id)+'/saved_state_dict.pt','rb')}
    
    response = requests.post(protocol+'://'+IP+'/api/upload_pytorch_weights', files=files, data={'run_id':run_id, 'username': username, 'key': key})


def load_torch_model(run_id):

    response = requests.post(protocol+'://'+IP+'/api/get_pytorch_weights', data={'run_id':run_id, 'username': username, 'key': key})
    response = response.json()

    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')

    if not os.path.exists('mynacode/'+str(run_id)):
      os.mkdir('mynacode/'+str(run_id))

    urllib.request.urlretrieve(response['weights'], 'mynacode/'+str(run_id)+'/'+response['weights'].split('/')[-1])
    urllib.request.urlretrieve(response['network'], 'mynacode/'+str(run_id)+'/'+response['network'].split('/')[-1])

    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'rb') as f:
        net = dill.load(f)


    net.load_state_dict(torch.load('mynacode/'+str(run_id)+'/saved_state_dict.pt'))

    return net


def save_file(run_id, filepath):
    if not os.path.exists(filepath):
      print(filepath, ' doesn not exist')
      return 
        
    file = {'file': open(filepath,'rb')}
    
    response = requests.post(protocol+'://'+IP+'/api/upload_file', files=file, data={'run_id':run_id, 'username': username, 'key': key})


def config(config_dict = {}, node_name="Datasets", run_id = None):

  if run_dir_global == "":
    print("Please run mynacode.start(...) before calling this function")
    return
  
  if not run_id:
    run_id = run_id_global

  if config_dict:
    file=open(run_dir_global+"/config.yaml","w")
    yaml.dump(config_dict,file)
    file.close()
    config_dict.update({'config_file': run_dir_global+"/config.yaml"})

  data = {'run_id' : run_id, 'config_dict': str(config_dict), 'node_name': node_name, 'username': username, 'key': key}
  
  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)


def torch_model(model=None, metric_name=None, metric_value=None, goal='maximize', run_id=None):
    global prev_min
    global prev_max
    global metric_values
    global metric_index
    global index_count

    if run_dir_global == "":
      print("Please run mynacode.start(...) before calling this function")
      return
    
    try:
        import torch
    except ImportError:
        print("Please install Pytorch before using this function.")
        return

    if not os.path.exists(run_dir_global+'/model'):
      os.mkdir(run_dir_global+'/model')

    config_dict = {}

    if model:
      with open(run_dir_global+'/model/saved_network.pkl', 'wb') as f:
          dill.dump(model, f)
          
      if goal == 'maximize':
        if metric_value > prev_max:
          metric_index = index_count
          prev_max = metric_value
          config_dict.update({'best_metric_value': metric_value})
          config_dict.update({'best_metric_index': metric_index})
          config_dict.update({'metric_goal': 'maximize'})
          
          if metric_name:
            torch.save(model.state_dict(), run_dir_global+'/model/best_'+str(metric_name)+'_'+str('%.4f' % metric_value)+'_chkpt.pt')
            config_dict.update({'best_weights_path': run_dir_global+'/model/best_'+str(metric_name)+'_'+str('%.4f' % metric_value)+'_chkpt.pt'})
            config_dict.update({'metric_name': metric_name})
          else:
            torch.save(model.state_dict(), run_dir_global+'/model/best_metric_'+str('%.4f' % metric_value)+'_chkpt.pt')
            config_dict.update({'best_weights_path': run_dir_global+'/model/best_metric_'+str('%.4f' % metric_value)+'_chkpt.pt'})
            
      elif goal == 'minimize':
        if metric_value < prev_min:
          metric_index = index_count
          prev_min = metric_value
          config_dict.update({'best_metric_value': metric_value})
          config_dict.update({'best_metric_index': metric_index})
          config_dict.update({'metric_goal': 'minimize'})
          
          if metric_name:
            torch.save(model.state_dict(), run_dir_global+'/model/best_'+str(metric_name)+'_'+str('%.4f' % metric_value)+'_chkpt.pt')
            config_dict.update({'best_weights_path': run_dir_global+'/model/best_'+str(metric_name)+'_'+str('%.4f' % metric_value)+'_chkpt.pt'})
            config_dict.update({'metric_name': metric_name})
          else:
            torch.save(model.state_dict(), run_dir_global+'/model/best_metric_'+str('%.4f' % metric_value)+'_chkpt.pt')
            config_dict.update({'best_weights_path': run_dir_global+'/model/best_metric_'+str('%.4f' % metric_value)+'_chkpt.pt'})

      metric_values.append(metric_value)
      index_count += 1
      config_dict.update({'metric_values': metric_values})
          
    else:
      print("Please specify a Pytorch model.")
      return

    results(results_dict = config_dict, run_id = None, node_name = 'Results')
    

def data(train_set=[], train_labels=[], test_set=[], test_labels=[], val_set=[], val_labels=[], save_once=True,
         problem_type = 'binary classification',  node_name="Datasets", run_id = None):


  if not run_id:
    run_id = run_id_global

  config_dict = {}
  
  train_set = np.array(train_set)
  val_set = np.array(val_set)
  test_set = np.array(test_set)

  if save_once == True:
    if project_dir_global == "":
      print("Please run mynacode.start(...) before calling this function")
      return
    current_dir = project_dir_global
  else:
    if run_dir_global == "":
      print("Please run mynacode.start(...) before calling this function")
      return
    current_dir = run_dir_global

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  if len(train_set) > 0:
    with open(current_dir+'/data/train_set.pkl', 'wb') as f:
        dill.dump(train_set, f)
    config_dict.update({'train_set': current_dir+'/data/train_set.pkl'})

  if len(val_set) > 0:
    with open(current_dir+'/data/val_set.pkl', 'wb') as f:
        dill.dump(val_set, f)
    config_dict.update({'val_set': current_dir+'/data/val_set.pkl'})

  if len(test_set) > 0:
    with open(current_dir+'/data/test_set.pkl', 'wb') as f:
        dill.dump(test_set, f)
    config_dict.update({'test_set': current_dir+'/data/test_set.pkl'})

  train_labels = np.array(train_labels)
  val_labels = np.array(val_labels)
  test_labels = np.array(test_labels)

  if len(train_labels) > 0:
    train_unique, train_count = np.unique(train_labels, return_counts=True)
    config_dict.update({'train_labels': train_unique.tolist(), 'train_count':train_count.tolist()})
    with open(current_dir+'/data/train_labels.pkl', 'wb') as f:
        dill.dump(train_labels, f)

  if len(val_labels) > 0:
    val_unique, val_count = np.unique(val_labels, return_counts=True)
    config_dict.update({'val_labels': val_unique.tolist(), 'val_count':val_count.tolist()})
    with open(current_dir+'/data/val_labels.pkl', 'wb') as f:
        dill.dump(val_labels, f)

  if len(test_labels) > 0:
    test_unique, test_count = np.unique(test_labels, return_counts=True)
    config_dict.update({'test_labels': test_unique.tolist(), 'test_count':test_count.tolist()})
    with open(current_dir+'/data/test_labels.pkl', 'wb') as f:
        dill.dump(test_labels, f)

      
  data = {'run_id' : run_id, 'config_dict': str(config_dict), 'node_name': node_name, 'username': username, 'key': key}
  
  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)


def torch_data(train_dataloader=None, val_dataloader=None, test_dataloader=None, save_once=True, label_index=None,
         problem_type = 'binary classification',  node_name="Datasets", run_id = None):

  if not run_id:
    run_id = run_id_global

  config_dict = {}

  if save_once == True:
    if project_dir_global == "":
      print("Please run mynacode.start(...) before calling this function")
      return
    current_dir = project_dir_global
  else:
    if run_dir_global == "":
      print("Please run mynacode.start(...) before calling this function")
      return
    current_dir = run_dir_global

  if not os.path.exists(current_dir+'/data'):
    os.mkdir(current_dir+'/data')

  if train_dataloader:
    if label_index:
      train_labels = [np.array(train_dataloader.dataset[i][label_index]) for i in range(len(train_dataloader.dataset))]
      with open(current_dir+'/data/train_dataloader.pkl', 'wb') as f:
          dill.dump(train_dataloader, f)
      config_dict.update({'train_dataloader': current_dir+'/data/train_dataloader.pkl'})

  if val_dataloader:
    if label_index:
      val_labels = [np.array(val_dataloader.dataset[i][label_index]) for i in range(len(val_dataloader.dataset))]
      with open(current_dir+'/data/val_dataloader.pkl', 'wb') as f:
          dill.dump(val_dataloader, f)
      config_dict.update({'val_dataloader': current_dir+'/data/val_dataloader.pkl'})

  if test_dataloader:
    if label_index:
      test_labels = [np.array(test_dataloader.dataset[i][label_index]) for i in range(len(test_dataloader.dataset))]
      with open(current_dir+'/data/test_dataloader.pkl', 'wb') as f:
          dill.dump(test_dataloader, f)
      config_dict.update({'test_dataloader': current_dir+'/data/test_dataloader.pkl'})

  train_labels = np.array(train_labels)
  val_labels = np.array(val_labels)
  test_labels = np.array(test_labels)

  if len(train_labels) > 0:
    train_unique, train_count = np.unique(train_labels, return_counts=True)
    config_dict.update({'train_labels': train_unique.tolist(), 'train_count':train_count.tolist()})

  if len(val_labels) > 0:
    val_unique, val_count = np.unique(val_labels, return_counts=True)
    config_dict.update({'val_labels': val_unique.tolist(), 'val_count':val_count.tolist()})

  if len(test_labels) > 0:
    test_unique, test_count = np.unique(test_labels, return_counts=True)
    config_dict.update({'test_labels': test_unique.tolist(), 'test_count':test_count.tolist()})

  if not run_id:
    run_id = run_id_global
      
  data = {'run_id' : run_id, 'config_dict': str(config_dict), 'node_name': node_name, 'username': username, 'key': key}
  
  response = requests.post(protocol+'://'+IP+'/api/add_data', data=data)






  




 



