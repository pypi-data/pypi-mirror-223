import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from sklearn.preprocessing import LabelEncoder
import pdcast as pdc
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size1,hidden_size2, output_size):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size2, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu1(out)
        out = self.fc2(out)
        out = self.relu2(out)
        out = self.fc3(out)
        out = self.sigmoid(out)
        return out
    
def getdata(name):
    if(name=='compas'):
        input_size=3
        use_cols = ['race', 'priors_count', 'age_cat', 'c_charge_degree','two_year_recid']
        data = pd.read_csv("https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv",
                usecols=use_cols)

        data = data.dropna(axis=0, how='any')

        value_mapper = {"Less than 25":0,"25 - 45":1,"Greater than 45":2}
        data["age_cat"] = data["age_cat"].replace(value_mapper)

        # label encoding protected_attribute and label
        label = 'two_year_recid'
        protected_attributes = ['race']
        cols_to_labelencode = protected_attributes.copy()
        cols_to_labelencode.append(label)
        data[cols_to_labelencode] = data[cols_to_labelencode].apply(LabelEncoder().fit_transform)
        # one-hot encoding categorical columns
        categorical_cols = list(data.select_dtypes(include='object'))
        data = pd.get_dummies(data, columns=categorical_cols)
        # downcast
        data = pdc.downcast(data)
        data.loc[data["priors_count"] < 10 , "priors_count"] = 0
        data.loc[(data["priors_count"] >= 10) & (data["priors_count"] < 25 ), "priors_count"] = 1
        data.loc[data["priors_count"] >= 25 , "priors_count"] = 2

        protected_attributes1 = ["race","priors_count","age_cat"]
        protected_attributes2 = protected_attributes1
        return data, protected_attributes1, protected_attributes2, input_size,'two_year_recid'
    
    elif(name== 'adult'):
        input_size =3
        data = pd.read_table(r"C:\Users\alhom\Desktop\BA\adult.data",delimiter=',', header=None,
        names=["age", "workclass", "fnlwgt", "education","education-num", "marital-status",
        "occupation", "relationship", "race", "sex","capital-gain", "capital-loss",
        "hours-per-week", "native-country", "income"])

        cols_to_drop = ['fnlwgt', 'workclass', 'education', 'occupation','native-country',"capital-gain", "capital-loss","hours-per-week"]
        data = data.drop(columns=cols_to_drop)

        data.loc[data["age"] < 30 , "age"] = 0
        data.loc[(data["age"] >= 30) & (data["age"] < 50 ), "age"] = 1
        data.loc[data["age"] >= 50 , "age"] = 2

        data["income"] = data["income"].astype(str)

        data["income"] = data["income"].replace({'<=50K': 0 ,'>50K': 1},regex=True)
        data['race'] = data[['race']].apply(LabelEncoder().fit_transform)
        data['sex'] = data[['sex']].apply(LabelEncoder().fit_transform)

        columns = ['race','age','sex']
        protected_attributes1 = data[columns].columns.tolist()
        protected_attributes2 = ['sex','race','age','income']
        return data, protected_attributes1, protected_attributes2, input_size,'income'

    elif(name =='bank'):
        input_size = 3
        data = pd.read_csv(r"C:\Users\alhom\Desktop\BA\bank-additional-full.csv", header=None,sep=';',names=["age", "job", "marital", "education","default", "housing","loan","contact",
        "month", "day_of_week", "duration","campaign", "pdays",
        "previous", "poutcome", "emp.var.rate","cons.price.idx","cons.conf.idx","euribor3m","nr.employed","Output variable"]).reset_index()
        data = data.iloc[1:]

        data['job'] = data[['job']].apply(LabelEncoder().fit_transform)
        data=data.dropna(subset=['loan'])

        data["age"] = data["age"].astype(int)

        data.loc[data["age"] < 30 , "age"] = 0
        data.loc[(data["age"] >= 30) & (data["age"] < 50 ), "age"] = 1
        data.loc[data["age"] >= 50 , "age"] = 2


        data['loan'] = data['loan'].map({"no":0,"yes":1,"unknown":2}).astype(int)
        data['Output variable'] = data['Output variable'].map({"no":0,"yes":1}).astype(int)
        data['housing'] = data['housing'].map({"no":0,"yes":1,"unknown":2}).astype(int)
        data['contact'] = data['contact'].map({"cellular":0,"telephone":1}).astype(int)
        cols_to_drop = ['euribor3m', 'cons.conf.idx', 'nr.employed', 'cons.price.idx','emp.var.rate',"previous", "poutcome", "emp.var.rate","cons.price.idx","cons.conf.idx"]
        data = data.drop(columns=cols_to_drop)

        value_mapping = {'basic.4y':0,'high.school':1,'basic.6y':0,'basic.9y':0, 'professional.course': 1,'university.degree':1, 'unknown': 0, 'illiterate' : 0}
        data["education"] = data["education"].replace(value_mapping)

        value_mapping1 = {'married':0,'single':1,'divorced':2,'unknown':3}
        data["marital"] = data["marital"].replace(value_mapping1)        
        protected_attributes1 = ['age','education','marital']
        protected_attributes2 = ["age","job","education","Output variable"]
        return data, protected_attributes1, protected_attributes2, input_size,'Output variable'

    elif(name=='ccc'):
        input_size =3
        data = pd.read_excel(r'C:\Users\alhom\Desktop\BA\credit_card.xls', index_col=0)
        cols_to_drop = ['X6', 'X7', 'X8', 'X9','X10','X11','X12','X13','X14','X15','X16','X17','X18','X19','X20','X21','X22','X23']
        data = data.drop(columns=cols_to_drop)

        data.rename(columns = {'X2':'sex','X3':'education','X4':'marriage','X5':'age'},inplace =True)
        data = data.iloc[1:]
        data = data[data["education"] <=3]

        data["sex"] =data["sex"].astype(int)
        data["education"] = data["education"].astype(int)
        data["marriage"]= data["marriage"].astype(int)
        data["Y"]= data["Y"].astype(int)
        protected_attributes1 = ['sex','education','marriage']
        protected_attributes2 = ['sex','education','marriage','default_payment']
        return data, protected_attributes1, protected_attributes2, input_size, 'Y'

    else:
        input_size = 2
        data = pd.read_csv(r"C:\Users\alhom\Desktop\BA\studentInfo.csv", header=None,sep=',',names=["code_module", "code_pres", "id_student", "gender","region","heighest_edu", "imd","age_band","num_of_prev_attempt",
        "studied_credits", "disability", "final_result"]).reset_index()
        data = data.iloc[1:]
        data=data.dropna(subset=['imd'])
        value_mapping = {'F':0,'M':1}
        data["gender"] = data["gender"].replace(value_mapping)
        value_mapping2 = {'55<=':2,'35-55':1,'0-35':0}
        data["age_band"] = data["age_band"].replace(value_mapping2)

        value_mapping3 = {'Fail':0,'Withdrawn':0,'Pass':1,'Distinction':1}
        data["final_result"] = data["final_result"].replace(value_mapping3)

        print("Data",data.columns)

        #encoded_data = pd.get_dummies(data, columns=['gender','age_band'])
        #data = encoded_data
        print(data.columns)
        columns = ['gender','age_band']
        protected_attributes1 = data[columns].columns.tolist()
        protected_attributes2 = ['gender','age_band','final_result']
        return data, protected_attributes1, protected_attributes2, input_size, 'final_result'
    
def calculate_multi_predictive_parity(predictions, labels,y_test ,sensitive_attributes, SA_list,weight=0):

    predictions = predictions.detach().reshape(-1,1).squeeze()
    y_test = y_test.detach().reshape(-1,1).squeeze()

    sensitive_attributes = sensitive_attributes.T

    dict_attributes = {}

    for attribute, p in zip(SA_list,range(len(sensitive_attributes))):
        dict_attributes[attribute] = (sensitive_attributes[p])

    max_diff = torch.tensor(0.0) 
    diff = 0.0

    for key in dict_attributes:
        groups = torch.unique(dict_attributes[key])
        max_diff1 = torch.tensor(0.0)  
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                
                numerator_1 = torch.sum((predictions >= 0.5) & (dict_attributes[key] == groups[i]) & (~y_test))
                denominator_1 = torch.sum((dict_attributes[key] == groups[i]) & (~y_test))
                numerator_2 = torch.sum((predictions >= 0.5) & (dict_attributes[key] == groups[j])& (~y_test))
                denominator_2 = torch.sum((dict_attributes[key] == groups[j]) & (~y_test))
                diff = torch.abs((numerator_1.float() / denominator_1.float()) - (numerator_2.float() / denominator_2.float()))
                #print("diff",diff)
                if weight == 1:
                    diff = diff * (1 - torch.abs(torch.sum(dict_attributes[key] == groups[i]) - torch.sum(dict_attributes[key] == groups[j]))/ (torch.sum(dict_attributes[key] == groups[i]) + torch.sum(dict_attributes[key] == groups[j])))
                max_diff1 = diff if diff > max_diff1 else max_diff1
        max_diff += max_diff1
    return max_diff / len(dict_attributes)


def calculate_multi_statistical_parity(predictions, labels, sensitive_attributes, SA_list,weight=0):

    predictions = predictions.detach().reshape(-1,1).squeeze()

    sensitive_attributes = sensitive_attributes.T
    dict_attributes = {}

    for attribute, p in zip(SA_list,range(len(sensitive_attributes))):
        dict_attributes[attribute] = (sensitive_attributes[p])

    max_diff = torch.tensor(0.0) 
    diff = 0.0
    for key in dict_attributes:
        groups = torch.unique(dict_attributes[key])
        max_diff1 = torch.tensor(0.0)  
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                
                numerator_1 = torch.sum((predictions >= 0.5) & (dict_attributes[key] == groups[i]))
                denominator_1 = torch.sum(dict_attributes[key] == groups[i])
                numerator_2 = torch.sum((predictions >= 0.5) & (dict_attributes[key] == groups[j]))
                denominator_2 = torch.sum(dict_attributes[key] == groups[j])
                diff = torch.abs((numerator_1.float() / denominator_1.float()) - (numerator_2.float() / denominator_2.float()))
                if weight == 1:
                    diff = diff * (1 - torch.abs(torch.sum(dict_attributes[key] == groups[i]) - torch.sum(dict_attributes[key] == groups[j]))/ (torch.sum(dict_attributes[key] == groups[i]) + torch.sum(dict_attributes[key] == groups[j])))
                max_diff1 = diff if diff > max_diff1 else max_diff1
        max_diff += max_diff1
    return max_diff / len(dict_attributes)

def calculate_multi_statistical_parity_testset(labels, sensitive_attributes, SA_list,weight=0):

    labels = labels.detach().reshape(-1,1).squeeze()

    sensitive_attributes = sensitive_attributes.T
    dict_attributes = {}

    for attribute, p in zip(SA_list,range(len(sensitive_attributes))):
        dict_attributes[attribute] = (sensitive_attributes[p])

    max_diff = torch.tensor(0.0) 
    diff = 0.0
    for key in dict_attributes:
        groups = torch.unique(dict_attributes[key])
        max_diff1 = torch.tensor(0.0)  
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                
                numerator_1 = torch.sum((labels) & (dict_attributes[key] == groups[i]))
                denominator_1 = torch.sum(dict_attributes[key] == groups[i])
                numerator_2 = torch.sum((labels) & (dict_attributes[key] == groups[j]))
                denominator_2 = torch.sum(dict_attributes[key] == groups[j])
                diff = torch.abs((numerator_1.float() / denominator_1.float()) - (numerator_2.float() / denominator_2.float()))
                if weight == 1:
                    diff = diff * (1 - torch.abs(torch.sum(dict_attributes[key] == groups[i]) - torch.sum(dict_attributes[key] == groups[j]))/ (torch.sum(dict_attributes[key] == groups[i]) + torch.sum(dict_attributes[key] == groups[j])))
                max_diff1 = diff if diff > max_diff1 else max_diff1
        max_diff += max_diff1
    return max_diff / len(dict_attributes)

def splitData(name):
    data, SA_List, protected, input_size,truth = getdata(name)
    sensitive = []
    for k in list(SA_List):
        sensitive.append(data[k]) 
    X_train, X_test, y_train, y_test = train_test_split(np.array(sensitive).T, np.array(data[[truth]]), test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test,data, SA_List, protected, input_size,np.array(data[[truth]])

# Unweighted LOSS SP
def Calculate_Dependency(name,SP=0):
    # Example usage:
    X_train, X_test, y_train, y_test,data, SA_List, protected, input_size,truth =splitData(name)

    hidden_size1 = 20
    hidden_size2 = 10
    output_size = 1

    # Initialize the model
    #model = NeuralNetwork(input_size, hidden_size1 ,hidden_size2 ,output_size)

    # Define the loss function
    #criterion = nn.BCELoss()

    # Define the optimizer
    #optimizer = optim.SGD(model.parameters(), lr=0.01)

    input_data = torch.from_numpy(X_train).float()
    X_test = torch.from_numpy(X_test).float()
    labels = torch.from_numpy(y_train).float()
    y_test = torch.from_numpy(y_test).int()


    labels = labels.reshape(-1,1)
    # Training loop
    num_epochs = 100

    accs = []
    accs2 = []

    Unweighted_SP_LOSS_weighted_SP_Dep = []
    Unweighted_SP_LOSS_Unweighted_SP_Dep = []

    Unweighted_SP_LOSS_weighted_PP_Dep = []
    Unweighted_SP_LOSS_Unweighted_PP_Dep = []

    Test_set_unweighted_SP =  calculate_multi_statistical_parity_testset(y_test, X_test, SA_List,weight=0)
    Test_set_weighted_SP = calculate_multi_statistical_parity_testset(y_test, X_test, SA_List,weight=1)
    

    if(SP):
        disc_regularization = 0.1
        

        while(disc_regularization < 1.1):

            model = NeuralNetwork(input_size, hidden_size1 ,hidden_size2 ,output_size)

            # Define the loss function
            criterion = nn.BCELoss()

            # Define the optimizer
            optimizer = optim.SGD(model.parameters(), lr=0.01)

            a = []
            b = []
            c = []
            d = []
            acc = []

            print(disc_regularization)
            for i in range(10):

                print("i",i)
                for epoch in range(num_epochs):

                    outputs = model(input_data)

                    # Compute discrimination
                    disc_loss = calculate_multi_statistical_parity(outputs, y_test, input_data,SA_List)

                    # Compute the loss with discrimination
                    loss = (1-disc_regularization) * criterion(outputs,labels) + disc_regularization * disc_loss
                    #print("loss",loss)

                        # Backward and optimize
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                X_test = torch.tensor(X_test, dtype=torch.float32)    

                # Use the trained model for prediction
                with torch.no_grad():
                    predictions = model(X_test)
                    predicted_labels = (predictions >= 0.5).float()

                    unweighted_1 = calculate_multi_statistical_parity(predictions, y_test, X_test, SA_List)
                    weighted_1 = calculate_multi_statistical_parity(predictions, y_test, X_test, SA_List,1)
                    unweighted_2 = calculate_multi_predictive_parity(predictions, labels,y_test, X_test, SA_List)
                    weighted_2 = calculate_multi_predictive_parity(predictions, labels,y_test, X_test, SA_List,1)

                    a.append(unweighted_1)
                    b.append(weighted_1)
                    c.append(unweighted_2)
                    d.append(weighted_2)

                    accuracy = (predicted_labels == y_test).float().mean()
                    acc.append(accuracy)
                # Calculate accuracy
                
                print("accuracy",accuracy)
            accs.append(np.mean(acc))
            Unweighted_SP_LOSS_Unweighted_SP_Dep.append(np.mean(a))
            Unweighted_SP_LOSS_weighted_SP_Dep.append(np.mean(b))
            Unweighted_SP_LOSS_Unweighted_PP_Dep.append(np.mean(c))
            Unweighted_SP_LOSS_weighted_PP_Dep.append(np.mean(d))

            disc_regularization += 0.1

        return Unweighted_SP_LOSS_Unweighted_SP_Dep, Unweighted_SP_LOSS_weighted_SP_Dep, Unweighted_SP_LOSS_Unweighted_PP_Dep, Unweighted_SP_LOSS_weighted_PP_Dep, \
            accs,Test_set_unweighted_SP,Test_set_weighted_SP

def getFigs(name):
    #print("HERE")
    Unweighted_SP_LOSS_Unweighted_SP_Dep_compas, Unweighted_SP_LOSS_weighted_SP_Dep_compas, Unweighted_SP_LOSS_Unweighted_PP_Dep_compas, Unweighted_SP_LOSS_weighted_PP_Dep_compas, \
         accs_compas,Test_set_unweighted_SP_compas,Test_set_weighted_SP_compas = Calculate_Dependency(name,1)
    
    fig = plt.figure(figsize=(5,4))
    ax = fig.add_axes([1,1,1,1])

    plt.plot(np.arange(0,1.1,0.1),Unweighted_SP_LOSS_Unweighted_SP_Dep_compas,linewidth=4,label= "Unweighted Approach 1")
    plt.plot(np.arange(0,1.1,0.1),Unweighted_SP_LOSS_weighted_SP_Dep_compas,linewidth=4,linestyle="dotted",label = "Weighted Approach 1")

    plt.plot(np.arange(0,1,0.1),Unweighted_SP_LOSS_Unweighted_PP_Dep_compas[:10],linewidth=4,linestyle="dashed",label= "Unweighted Approach 2")
    plt.plot(np.arange(0,1,0.1),Unweighted_SP_LOSS_weighted_PP_Dep_compas[:10],linewidth=4,linestyle="dashdot",label= "Weighted Approach 2")

    plt.xticks(np.arange(0,1.2,0.1))
    plt.ylabel("Dependency",fontsize=17)
    plt.legend()
    plt.xlabel("Trade-Off Parameter (Alpha)",fontsize = 17)

    #plt.savefig(r'C:\Users\alhom\Desktop\BA\vorlage_2020_08_19\bilder\NN_' + name + r'\NN' + name + r'FairNNDep.pdf', bbox_inches='tight')
    plt.savefig(r'C:\Users\alhom\Desktop\BA\test\\' + name + r'FairNNDep.pdf', bbox_inches='tight')
    #plt.savefig(r'NN' + name + r'FairNNDep.pdf', bbox_inches='tight')
    plt.show()


    dim = 2
    w = 1
    dimw = w / dim

    fig = plt.figure(figsize=(5,4))
    ax = fig.add_axes([1,1,1,1])
    x = np.arange(2)

    y = [float(Test_set_unweighted_SP_compas.item()), float(Test_set_weighted_SP_compas.item())]


    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    ax.bar(x, y, dimw, bottom=0.001, color=default_colors[:2])
    plt.ylabel("Dependency", fontsize=17)
    ax.set_xticks(x)
    plt.xticks(fontsize=10, ha="center")
    ax.set_xticklabels(["Unweighted SP","Weighted SP"], fontsize=10, ha="center")
    #plt.savefig(r'C:\Users\alhom\Desktop\BA\vorlage_2020_08_19\bilder\NN_'+ name + r'\NN'+ name+ r'YandZDep.pdf', bbox_inches='tight')
    plt.savefig(r'C:\Users\alhom\Desktop\BA\test\\'+ name+ r'YandZDep.pdf', bbox_inches='tight')
    #plt.savefig(r'NN'+ name+ r'YandZDep.pdf', bbox_inches='tight')
    plt.show()



    plt.plot(np.arange(0,1.1,0.1),accs_compas)
    #plt.bar(1,accs2_compas,0.05,label = "Unfair NN",color = "orange")
    plt.ylabel("Accuracy",fontsize=17)
    plt.xlabel("Trade-Off Parameter (Alpha)",fontsize=17)

    #plt.savefig(r'C:\Users\alhom\Desktop\BA\vorlage_2020_08_19\bilder\NN_'+ name+ r'\NN'+ name+ r'FairUnfairNNAcc.pdf', bbox_inches='tight')
    plt.savefig(r'C:\Users\alhom\Desktop\BA\test\\'+ name+ r'FairUnfairNNAcc.pdf', bbox_inches='tight')
    #plt.savefig(r'NN'+ name+ r'FairUnfairNNAcc.pdf', bbox_inches='tight')
    plt.show()
    
getFigs('ccc')
getFigs('adult')
getFigs('bank')
getFigs('compas')
getFigs('uni')