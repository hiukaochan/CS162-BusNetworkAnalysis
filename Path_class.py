import json
import csv

class Path:
    def __init__(self,dict):
        self.lat = dict['lat']
        self.lng = dict['lng']
        self.RouteId = dict['RouteId']
        self.RouteVarId = dict['RouteVarId']
        self.AllData = dict

    def getter(self, properties):
        return self.AllData[properties]
    def getterAll(self):
        return self.AllData
    
    def setter(self, properties, val):
        self.AllData[properties] = val
        self.lat = self.AllData['lat']
        self.lng = self.AllData['lng']
        self.RouteId = self.AllData['RouteId']
        self.RouteVarId = self.AllData['RouteVarId']

    def to_dict(self):
        typedict = {'lat':self.lat,'lng':self.lng,'RouteId':self.RouteId,'RouteVarId':self.RouteVarId}
        return typedict

class PathQuery:
    def __init__(self,Path_list):
        self.query_data = Path_list
    
    def searchByABC(self,properties,value):
        SearchResult = []
        for eachPath in self.query_data:
            if eachPath.getter(properties) == value: SearchResult.append(eachPath)
        return SearchResult
    
    def outputAsJSON(self, list, filename):
        with open(filename, "w", encoding='utf-8') as fileJSON:
            fileJSON.write( '[' + ',\n'.join (json.dumps(eachlist.to_dict(), ensure_ascii=False) for eachlist in list) + ']\n')
    
    def outputAsCSV(self,list,filename):
        field = ['lat','lng','RouteId','RouteVarId']
        with open(filename,"w",encoding='utf-8') as fileCSV:
            writer = csv.DictWriter(fileCSV, fieldnames=field)
            writer.writeheader()
            for eachlist in list: 
                writer.writerow(eachlist.to_dict())
