import pyproj
from pyproj import Transformer
import json
import shapely
import math
import heapq
from timeit import default_timer as timer
import time
import openai

#from RouteVar_class import RouteVar,RouteVarQuery
from Stop_class import Stop, StopQuery
from Path_class import Path, PathQuery

def get_gorilla_response(prompt="", model="gorilla-openfunctions-v2", functions=[]):
  openai.api_key = "EMPTY"
  openai.api_base = "http://luigi.millennium.berkeley.edu:8000/v1"
  try:
    completion = openai.ChatCompletion.create(
      model="gorilla-openfunctions-v2",
      temperature=0.0,
      messages=[{"role": "user", "content": prompt}],
      functions=functions,
    )
    return completion.choices[0]
  except:
    print("ERROR OCCURRED.")

function_documentation = [] 

with open("function_doc.json") as invoke_api:
    for eachline in invoke_api:
        tmp_dic = json.loads(eachline)
        function_documentation.append(tmp_dic)

#IN-USE FUNCTIONS 

def combine_var_id(x,y):
    return str(x) + "," + str(y)

def calc_distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

#CONVERT LAT,LNG TO X,Y

source_proj = pyproj.CRS.from_epsg(4326) #Earth's center of mass
target_proj = pyproj.CRS.from_epsg(3405) #Vietnam 48N
transformer = pyproj.Transformer.from_crs(source_proj, target_proj, always_xy=True)

def latlng_to_xy(lat, lng):
    x, y = transformer.transform(lng, lat)
    return x, y

#CREATE A DICTIONARY TO STORE LAT,LNG FOR EACH STOP AND AN ARRAY TO STORE POSITION OF STOPS FOR BUILDING NODE

Stop_pos = {}
cntStop = 0

track_stop_from_pos = [] 

with open("stops.json") as filestops:
    for eachline in filestops:
        data = json.loads(eachline)
        datalist = data['Stops']
        for eachdata in data['Stops']:
            mydict = eachdata
            s = Stop(mydict)
            if Stop_pos.get(str(s.StopId)) is None: 
                Stop_pos.update({str(s.StopId):{'Pos':cntStop,'Stop':mydict}})
                track_stop_from_pos.append(s.StopId)
                cntStop = cntStop + 1 

adlist = {}

#Adjacency list
for i in range(0,cntStop):
    adlist.update({str(i):{}})

Path_pos = {}

with open("paths.json") as filepaths:
    for eachline in filepaths:
        data = json.loads(eachline)
        mypath = Path(data)
        Path_pos.update({combine_var_id(mypath.RouteId,mypath.RouteVarId):{"Lat":mypath.lat,"Lng":mypath.lng}})

with open("edge.json") as filejson1:
    adlist = json.load(filejson1)

#DIJKSTRA PERFORMANCE

dp = []
trace = []
for i in range(0, cntStop):
    dp.append([])
    trace.append([])  

def dijkstra(source_node):
    for i in range(0, cntStop):
        dp[source_node].append(1000000000000)
        trace[source_node].append(0)
    
    dp[source_node][source_node] = 0

    pq = [(0,source_node)] #Queue

    while pq:
        current_time, current_node = heapq.heappop(pq)
        if current_time > dp[source_node][int(current_node)]:
            continue
        for node, value in adlist[str(current_node)].items():
            cost, distance,name,startid,endid = value
            if dp[source_node][int(node)] > dp[source_node][int(current_node)] + cost:
                trace[source_node][int(node)] = (current_node,name,startid,endid)
                dp[source_node][int(node)] = dp[source_node][int(current_node)] + cost
                heapq.heappush(pq,(dp[source_node][int(node)],int(node)))

for i in range(0,cntStop):
    dijkstra(i)

#WRITE 1 PAIR PATH TO DIJKSTRA_QUERY.JSON
def fastest_route(start_stop:int,end_stop:int): #input StopId
    start_stop = Stop_pos[str(start_stop)]['Pos']
    end_stop = Stop_pos[str(end_stop)]['Pos']
    dict = {}
    dict.update({"Time": dp[start_stop][end_stop]})
    ans_Stop = []
    ans_Lat = []
    ans_Lng = []
    tmp_name = ""
    tmp_startidx = tmp_endidx = 0
    pos = end_stop
    while 1:
        if pos == start_stop:
            break
        ans_Stop.append(track_stop_from_pos[pos])
        tmp_pos, tmp_name, tmp_startidx, tmp_endidx = trace[start_stop][pos]
        for x in range(tmp_endidx,tmp_startidx,-1):
            ans_Lat.append(Path_pos[tmp_name]['Lat'][x])
            ans_Lng.append(Path_pos[tmp_name]['Lng'][x])
        pos = tmp_pos
    ans_Stop.append(track_stop_from_pos[start_stop])
    ans_Stop.reverse()
    ans_Lat.reverse()
    ans_Lng.reverse()
    dict.update({"Stop":ans_Stop,"lat":ans_Lat,"lng":ans_Lng})
    with open("ans.json", 'w', encoding = 'utf8') as fileJSON:
        fileJSON.write(json.dumps(dict))

#K MOST IMPORTANT NODES 

def k_importance(k):
    #make importance list
    importance = [0] * 5000
    for u in range(0, cntStop):
        for v in range(0, cntStop):
            if dp[u][v] == 1000000000000:
                continue
            pos = v
            while 1:
                importance[pos] = importance[pos] + 1
                if pos == u:
                    break
                pos, tmp_name, tmp_startidx, tmp_endidx = trace[u][pos]
    pq = []
    for i in range(0, cntStop):
        vt = track_stop_from_pos[i]
        heapq.heappush(pq, (-importance[i], vt))
    with open("K_stop.json", 'w', encoding = 'utf8') as jsonfile:
        for i in range(0, k):
            u, v = heapq.heappop(pq)
            ans = {"Importance no." : i + 1, "Stop": Stop_pos[str(v)]['Stop']}
            json.dump(ans, jsonfile, ensure_ascii=False)
            jsonfile.write('\n')

query = "Find fastest way to travel, starting from stop 3289 to 3934"
exec(get_gorilla_response(prompt=query, functions=[function_documentation]).message.content)