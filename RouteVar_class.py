import csv
import json

class RouteVar:
    def __init__(self, dict) :
        self.RouteId = dict['RouteId']
        self.RouteVarId = dict['RouteVarId']
        self.RouteVarName = dict['RouteVarName']
        self.RouteVarShortName = dict['RouteVarShortName']
        self.RouteNo = dict['RouteNo']
        self.StartStop = dict['StartStop']
        self.EndStop = dict['EndStop']
        self.Distance = dict['Distance']
        self.Outbound = dict['Outbound']
        self.RunningTime = dict['RunningTime']
        self.AllData = dict

    #Get functions
    def getter(self, properties):
        return self.AllData[properties]
    def getterAll(self):
        return self.AllData
    
    #Set functions
    def setter(self, properties, val):
        self.AllData[properties] = val
        self.RouteId = self.AllData['RouteId']
        self.RouteVarId = self.AllData['RouteVarId']
        self.RouteVarName = self.AllData['RouteVarName']
        self.RouteVarShortName = self.AllData['RouteVarShortName']
        self.RouteNo = self.AllData['RouteNo']
        self.StartStop = self.AllData['StartStop']
        self.EndStop = self.AllData['EndStop']
        self.Distance = self.AllData['Distance']
        self.Outbound = self.AllData['Outbound']
        self.RunningTime = self.AllData['RunningTime']

    def to_dict(self):
        typedict = {'RouteId':self.RouteId, 'RouteVarId':self.RouteVarId,'RouteVarName':self.RouteVarName,'RouteVarShortName':self.RouteVarShortName,'RouteNo':self.RouteNo,'StartStop':self.StartStop,'EndStop':self.EndStop,'Distance':self.Distance,'Outbound':self.Outbound,'RunningTime':self.RunningTime}
        return typedict

class RouteVarQuery:
    def __init__(self,RouteVar_list):
        self.query_data = RouteVar_list
    
    def searchByABC(self,properties,value):
        SearchResult = []
        for eachRouteVar in self.query_data:
            if eachRouteVar.getter(properties) == value: SearchResult.append(eachRouteVar)
        return SearchResult
    
    def outputAsJSON(self, list, filename):
        with open(filename, "w", encoding='utf-8') as fileJSON:
            fileJSON.write( '[' + ',\n'.join (json.dumps(eachlist.to_dict(), ensure_ascii=False) for eachlist in list) + ']\n')
    
    def outputAsCSV(self,list,filename):
        field = ["RouteId", "RouteVarId", "RouteVarName","RouteVarShortName","RouteNo","StartStop","EndStop","Distance","Outbound","RunningTime"]
        with open(filename,"w",encoding='utf-8') as fileCSV:
            writer = csv.DictWriter(fileCSV, fieldnames=field)
            writer.writeheader()
            for eachlist in list: 
                writer.writerow(eachlist.to_dict())




    