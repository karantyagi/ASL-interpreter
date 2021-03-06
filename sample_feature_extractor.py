import json
import numpy as np
import csv


with open('data_set/data32.txt') as data_file:
    f = json.load(data_file)

def averageArea():
    for item in f:
        t_s=0
        for k in range(len(item['data'])-1):
            s=0
            for i in range(1,5):
                s =(np.array(item['data'][k][str(i)]['mcpPosition']) + np.array(
                    item['data'][k][str(i+1)]['mcpPosition']))/2.0
                area=0.5*np.linalg.norm(np.cross(np.array(item['data'][k][str(i+1)]['tipPosition'])-np.array(item['data'][k][str(i)]['tipPosition']),s-np.array(item['data'][k][str(i)]['tipPosition'])))
            t_s+=area
        return t_s/(len(item['data']))


def averageSpread():
    for item in f:
        t_s=0
        for val in item['data']:
            s=0
            for i in range(1,5):
                s = np.sqrt(sum((np.array(val[str(i+1)]['tipPosition']) - np.array(val[str(i)]['tipPosition'])) ** 2))
            t_s+=s
        return t_s/len(item['data'])

def averageDistance():
    for item in f:
        t_s=0
        for k in range(len(item['data'])-1):
            s=0
            for i in range(1,6):
                s = np.sqrt(sum((np.array(item['data'][k+1][str(i)]['tipPosition']) - np.array(item['data'][k][str(i)]['tipPosition'])) ** 2))
            t_s+=s
        return t_s/(len(item['data'])-1)

def extended_distance(item,val,i):
    s=0
    if i == 1:
        tip_s = np.sqrt(sum((np.array(val[str(6)]['position']) - np.array(val[str(i)]['tipPosition'])) ** 2))
        dip_s = np.sqrt(sum((np.array(val[str(6)]['position']) - np.array(val[str(i)]['dipPosition'])) ** 2))
        pip_s = np.sqrt(sum((np.array(val[str(6)]['position']) - np.array(val[str(i)]['pipPosition'])) ** 2))
        s = max(np.linalg.norm(tip_s), np.linalg.norm(dip_s), np.linalg.norm(pip_s))
    else:
        tip_s = np.sqrt(
            sum((np.array(val[str(6)]['position']) - np.array(val[str(i)]['tipPosition'])) ** 2))
        dip_s = np.sqrt(
            sum((np.array(val[str(6)]['position']) - np.array(val[str(i)]['dipPosition'])) ** 2))
        pip_s = np.sqrt(
            sum((np.array(val[str(6)]['position']) - np.array(val[str(i)]['pipPosition'])) ** 2))
        mcp_s = np.sqrt(sum((np.array(val[str(6)]['position']) - np.array(val[str(i)]['mcpPosition'])) ** 2))
        s=max(np.linalg.norm(tip_s),np.linalg.norm(dip_s),np.linalg.norm(pip_s),np.linalg.norm(mcp_s))
    return s

def dip_tip_projection(item,val,i):
    vector_s = np.array(val[str(i)]['dipPosition']) - np.array(val[str(i)]['tipPosition'])
    scalar_vector= np.array(val[str(6)]['normal'])/np.linalg.norm(np.array(val[str(6)]['normal']))
    dot_vector= np.dot(vector_s,np.array(val[str(6)]['normal']))
    s = dot_vector*scalar_vector
    return s

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def angle(item,val,i):
    a=angle_between(np.array(val[str(i)]['direction']),np.array([1,0,1]))
    return a

def writecsv_cluster():
    with open('output_v.csv', 'wb') as o:
        w = csv.DictWriter(o, ['pinch_strength', 'grab_strength','average_distance','average_spread','average_trispread',
                               'f1_extended_distance','f1_diptip_projection','f1_angle','f2_extended_distance', 'f2_diptip_projection', 'f2_angle',
                               'f3_extended_distance', 'f3_diptip_projection', 'f3_angle','f4_extended_distance', 'f4_diptip_projection', 'f4_angle',
                               'f5_extended_distance', 'f5_diptip_projection', 'f5_angle','label'])

        w.writeheader()
        for item in f:
            for val in item['data']:
                elem={}
                for i in range(1, 6):
                    elem['pinch_strength']=val[str(6)]['pinch_strength']
                    elem['grab_strength'] = val[str(6)]['grab_strength']
                    elem['average_distance']=averageDistance()
                    elem['average_spread']=averageSpread()
                    elem['average_trispread']=averageArea()
                    elem['f'+str(i)+'_extended_distance']= extended_distance(item,val,i)
                    elem['f' + str(i) + '_diptip_projection'] = list(dip_tip_projection(item, val, i))
                    elem['f'+str(i)+'_angle']=angle(item, val, i)
                    elem['label']=item['label']
                w.writerow(elem)


writecsv_cluster()