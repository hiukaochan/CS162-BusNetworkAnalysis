import csv
import json

class Stop:
    def __init__(self, dict):
        self.StopId = dict['StopId']
        self.Code = dict['Code']
        self.Name = dict['Name']
        self.StopType = dict['StopType']
        self.Zone = dict['Zone']
        self.Ward = dict['Ward']
        self.AddressNo = dict['AddressNo']
        self.Street = dict['Street']
        self.SupportDisability = dict['SupportDisability']
        self.Status = dict['Status']
        self.Lng = dict['Lng']
        self.Lat = dict['Lat']
        self.Search = dict['Search']
        self.Routes = dict['Routes']
        #self.RouteId = dict['RouteId']
        #self.RouteVarId = dict['RouteVarId']
        self.AllData = dict

    def getter(self, properties):
        return self.AllData[properties]
    def getterAll(self):
        return self.AllData
    
    def setter(self, properties, val):
        self.AllData[properties] = val
        self.StopId = self.AllData['StopId']
        self.Code = self.AllData['Code']
        self.Name = self.AllData['Name']
        self.StopType = self.AllData['StopType']
        self.Zone = self.AllData['Zone']
        self.Ward = self.AllData['Ward']
        self.AddressNo = self.AllData['AddressNo']
        self.Street = self.AllData['Street']
        self.SupportDisability = self.AllData['SupportDisability']
        self.Status = self.AllData['Status']
        self.Lng = self.AllData['Lng']
        self.Lat = self.AllData['Lat']
        self.Search = self.AllData['Search']
        self.Routes = self.AllData['Routes']
        #self.RouteId = self.AllData['RouteId']
        #self.RouteVarId = self.AllData['RouteVarId']
    
    def to_dict(self):
        typedict = {'StopId':self.StopId,'Code':self.Code,'Name':self.Name,'StopType':self.StopType,'Zone':self.Zone,'Ward':self.Ward,'AddressNo':self.AddressNo,'Street':self.Street,'SupportDisability':self.SupportDisability,'Status':self.Status,'Lng':self.Lng,'Lat':self.Lat,'Search':self.Search,'Routes':self.Routes}
        return typedict
    
class StopQuery:
    def __init__(self,StopVar_list):
        self.query_data = StopVar_list
    
    def searchByABC(self,properties,value):
        SearchResult = []
        for eachStop in self.query_data:
            if eachStop.getter(properties) == value: SearchResult.append(eachStop)
        return SearchResult
    
    def outputAsJSON(self, list, filename):
        with open(filename, "w", encoding='utf-8') as fileJSON:
            fileJSON.write( '[' + ',\n'.join (json.dumps(eachlist.to_dict(), ensure_ascii=False) for eachlist in list) + ']\n')
    
    def outputAsCSV(self,list,filename):
        field = ['StopId','Code','Name','StopType','Zone','Ward','AddressNo','Street','SupportDisability','Status','Lng','Lat','Search','Routes']
        with open(filename,"w",encoding='utf-8') as fileCSV:
            writer = csv.DictWriter(fileCSV, fieldnames=field)
            writer.writeheader()
            for eachlist in list: 
                writer.writerow(eachlist.to_dict())