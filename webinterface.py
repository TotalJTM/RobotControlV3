from typing import Counter
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, session
from flask_session import Session
from flask_socketio import SocketIO
import json
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

socketio = SocketIO(app, manage_session=False)


class InterfaceObject:
    def __init__(self, id, header_text=None, value=None, display_round=5):
        self.id = id
        self.header_text = header_text
        self.value = value
        self.disp_round = display_round

    def to_dict(self):
        d = {
            'id':self.id,
            'value':self.value
        }
        if self.header_text:
            d['type'] = 'hdr'
            d['text'] = self.header_text
        else:
            d['type'] = 'nhdr'

        return d

    def to_display_dict(self):
        d = {
            'id':self.id,
        }
        if self.disp_round:
            d['value'] = f'{self.value:.{self.disp_round}f}'
        else:
            d['value'] = f'{self.value}'
        return d
  

class WebInterface:
    def __init__(self, name, groups):
        self.name = name
        self.interface_groups = []
        for group in groups: self.interface_groups.append(group) 

    def to_dict(self):
        d = {
            'groups':[]
        }
        for g in self.interface_groups:
            c = []
            for i in g['content']:
                c.append(i.to_dict())
            d['groups'].append({'label':g['label'],'name':g['name'],'content':c})
        return d

    def generate_display_dict(self):
        d = {
            'groups':[]
        }
        for g in self.interface_groups:
            c = []
            for i in g['content']:
                c.append(i.to_display_dict())
            d['groups'].append({'content':c})
        return d

    def update_interface(self, updated_objs):
        d = []
        for ob in updated_objs:
            d.append(ob.to_display_dict())
        #print(d)
        socketio.emit(f'{self.name}-update', d)

    def get_obj_by_name(self, groupname, objid):
        for group in self.interface_groups:
            if group['name'] == groupname:
                for obj in group['content']:
                    if obj.id == objid:
                        return obj
        
    def update_object_val(self, groupname, objid, newvalue, suppress_emit=False):
        for group in self.interface_groups:
            if group['name'] == groupname:
                for obj in group['content']:
                    if obj.id == objid:
                        obj.value = newvalue
                        disp_d = obj.to_display_dict()
                        socketio.emit(f'{self.name}-update', [disp_d])
                        if suppress_emit:
                            return (True, disp_d)
                        else:
                            return True
        return False

    # tuples = [(groupname, objid, newvalue),...]
    def update_object_vals(self, tuples):
        retarr = []
        for t in tuples:
            retarr.append(self.update_object_val(t[0], t[1], t[2], suppress_emit=True))
        socketio.emit(f'{self.name}-update', [i[1] for i in retarr])
        return retarr


num_demo = {
    'name':'num-demo',
    'label':'Number Demo',
    'content':[   
        InterfaceObject('s1','Stat 1',value=3,          display_round=None),
        InterfaceObject('s2','Stat 2',value=0.444444,   display_round=5),
        InterfaceObject('s3','Stat 3',value=0.000003333,display_round=8),
        InterfaceObject('s4','Stat 4',value=3,          display_round=2),
    ]
}

header_data = {
    'name':'header',
    'label':'',
    'content':[   
        InterfaceObject('connected-time','Instance Time',value=0,   display_round=0),
        InterfaceObject('textbar','Status',value='All be good!',    display_round=None),
    ]
}

wbintfc = WebInterface('mainpage', [header_data, num_demo])

global_th_flag = True

def adjust_values():
    counter = 0
    print("thread Started")
    while global_th_flag:
        x = wbintfc.get_obj_by_name('num-demo','s4')
        wbintfc.update_object_vals([
            ('num-demo','s1',counter),
            ('num-demo','s2',counter/0.02),
            ('num-demo','s4',x.value+0.33),
        ])
        #wbintfc.interface_items[0].value=counter
        #wbintfc.interface_items[1].value+=0.05
        #wbintfc.interface_items[3].value+=0.33
        #print(wbintfc.interface_items[0].to_dict())
        counter += 1
        #wbintfc.update_interface([wbintfc.interface_items[0],wbintfc.interface_items[1],wbintfc.interface_items[3]])

        #print(sensors_dict)
        time.sleep(0.15)
th_adjustvals = threading.Thread(target=adjust_values)
th_adjustvals.startedflag = False

def instance_clock():
    while global_th_flag:
        x = wbintfc.get_obj_by_name('header','connected-time')
        wbintfc.update_object_val('header','connected-time',x.value+1)
        time.sleep(1)
th_simpclock = threading.Thread(target=instance_clock)
th_simpclock.startedflag = False

@app.route('/')
def index():
    #d = wbintfc.generate_display_dict()

    if not th_adjustvals.startedflag:
        th_adjustvals.startedflag = True
        th_adjustvals.start()
        print('th_adjustvals started')

    if not th_simpclock.startedflag:
        th_simpclock.startedflag = True
        th_simpclock.start()
        print('th_simpclock started')

    wbintfc.update_object_val('header','connected-time',0)

    d = wbintfc.to_dict()
    session['groups'] = d['groups']
    return render_template('interfacedash.html')


if __name__ == "__main__":

    try:
        socketio.run(app)

    except KeyboardInterrupt:
        pass