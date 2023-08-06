import hashlib
import json
import os

class Chain():
    folder = ''
    error = []
    def __init__(self,folder='./data'):
        if os.path.isdir(folder) & os.path.isfile(folder+'/config.json'):
            self.folder = folder
        else:
            os.mkdir(folder)
            file = open(folder+'/config.json','w+')
            file.write(json.dumps({'total':'0'}))
            file.close()
            self.folder = folder

    def load(self,folder='./data'):
        if os.path.isdir(folder) & os.path.isfile(folder+'/config.json'):
            self.folder = folder
        else:
            os.mkdir(folder)
            file = open(folder+'/config.json','w+')
            file.write(json.dumps({'total':'0'}))
            file.close()
            self.folder = folder

    def check(self):
        with open(self.folder+'/config.json') as f:
            content = json.loads(f.read())
        total = int(content['total'])
        if total == 0:
            return True
        base = ''
        for num in range(1,total+1):
            with open(self.folder+'/'+str(num)+'.json') as f:
                source = json.loads(f.read())
            for i in range(0,len(source)):
                sha2 = hashlib.sha224('loongchain'.encode('utf-8'))
                if (base != source[i]['hash']) and (base != ''):
                    self.error.append(i-1)
                for key,value in source[i].items():
                    combine = '@'.join((key,value))
                    sha2.update(combine.encode('utf-8'))
                base = sha2.hexdigest()
        if len(self.error) == 0:
            return True
        else:
            return False

    def apply(self,record):
        with open(self.folder+'/config.json') as f:
            content = json.loads(f.read())
        total = int(content['total'])
        if total == 0:
            with open(self.folder+'/1.json','w+') as f:
                f.write(json.dumps([{'action':'create','hash':''}]))
            with open(self.folder+'/config.json','w+') as config:
                config.write(json.dumps({'total':'1'}))
            total = 1
        with open(self.folder+'/'+str(total)+'.json') as f:
            source = json.loads(f.read())
        if len(source) == 0:
            with open(self.folder+'/'+str(total-1)+'.json') as latest:
                oldata = json.loads(latest.read())
            sha2 = hashlib.sha224('loongchain'.encode('utf-8'))
            for key,value in oldata[-1].items():
                combine = '@'.join((key,value))
                sha2.update(combine.encode('utf-8'))
            record['hash'] = sha2.hexdigest()
            source.append(record)
        elif len(source) == 256:
            with open(self.folder+'/config.json','w+') as config:
                config.write(json.dumps({'total':str(total+1)}))
            total+=1
            sha2 = hashlib.sha224('loongchain'.encode('utf-8'))
            for key,value in source[-1].items():
                combine = '@'.join((key,value))
                sha2.update(combine.encode('utf-8'))
            record['hash'] = sha2.hexdigest()
            source = []
            source.append(record)
        else:
            sha2 = hashlib.sha224('loongchain'.encode('utf-8'))
            for key,value in source[-1].items():
                combine = '@'.join((key,value))
                sha2.update(combine.encode('utf-8'))
            record['hash'] = sha2.hexdigest()
            source.append(record)
        with open(self.folder+'/'+str(total)+'.json','w+') as f:
            f.write(json.dumps(source))
        f.close()

    def fetch(self,call):
        response = []
        with open(self.folder+'/config.json') as f:
            content = json.loads(f.read())
        total = int(content['total'])
        if total == 0:
            return response
        for num in range(1,total+1):
            with open(self.folder+'/'+str(num)+'.json') as f:
                source = json.loads(f.read())
            for i in range(0,len(source)):
                for key,value in call.items():
                    sign = False
                    if key in source[i].keys():
                        if source[i][key] == value:
                            sign = True
                if sign:
                    response.append(source[i])
        return response

    def run(self,obj):
        with open(self.folder+'/config.json') as f:
            content = json.loads(f.read())
        total = int(content['total'])
        if total == 0:
            return False
        for num in range(1,total+1):
            with open(self.folder+'/'+str(num)+'.json') as f:
                source = json.loads(f.read())
            for record in source:
                obj.do(record)

    def log(self,msg,type='normal'):
        style = {'error':'31','safe':'32','warn':'33','info':'34','normal':'38'}
        print('\033['+style[type]+'m'+msg+'\033[0m')