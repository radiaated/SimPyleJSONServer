from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import sys
from urllib.parse import urlparse, parse_qs
from uuid import uuid1
import os

def json_path_formatter(path):
    if path[0] != "/":
        path = "/" + path
    
    return path

def path_formatter(path):
    if path[0] == "/":
        path = path[1:]

    return path

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
try: 

    f = open("settings.json", "r")
    set_json = json.load(f)
    f.close()
    hostName = "localhost"
    serverPort = set_json["serverPort"]
    staticPath = set_json["staticPath"]
    jsonPath = set_json["jsonPath"]

    if (len(sys.argv) > 1):
        userParam = dict()
        for i in range(1, len(sys.argv)):
            if sys.argv[i].split("=")[0] == "path":
                userParam["path"] = json_path_formatter(sys.argv[i].split("=")[1])
            elif sys.argv[i].split("=")[0] == "json":
                userParam["json"] = sys.argv[i].split("=")[1]
            elif sys.argv[i].split("=")[0] == "port":
                
                set_json["serverPort"] = int(sys.argv[i].split("=")[1])
                serverPort = int(sys.argv[i].split("=")[1])
                
            elif sys.argv[i].split("=")[0] == "json_path":
                
                set_json["jsonPath"] = sys.argv[i].split("=")[1]
                jsonPath = sys.argv[i].split("=")[1]
                
            elif sys.argv[i].split("=")[0] == "static_path":
                
                set_json["staticPath"] = sys.argv[i].split("=")[1]
                staticPath = sys.argv[i].split("=")[1]
                
            elif sys.argv[i].split("=")[0] == "rm-path":
                
                set_json["endpoints"] = [item for item in set_json["endpoints"] if item["path"] != sys.argv[i].split("=")[1]]
                
            elif sys.argv[i].split("=")[0] == "view":
                for epp in set_json["endpoints"]:
                    print(f'[Path: {epp["path"]}] > [JSON: {epp["json"]}]')
            else:
                print(f"Invalid argument: " + sys.argv[i].split("=")[0])

        if userParam.get("path"):
            q = [p for p in set_json["endpoints"] if p["path"] != userParam["path"]]
            q.append(userParam)
            print(f'[Path: {userParam["path"]}] > [JSON: {userParam["json"]}]')
            set_json["endpoints"] = q

        f = open("settings.json", "w")
        json.dump(set_json, f)
        f.close()

    endpoints = set_json["endpoints"]
except:
    print("Error occured. Issue may be in settings.json or the argument in the command 'python server.py'.")
            
def props_getter(spl_path, i, dataa, post_data, method):
    
    if i == len(spl_path) - 1:
        if method == "POST":
            form22 = dict()
            for key in post_data.keys():
                if isinstance(post_data[key], list):
                    temp = list()
                    for item in post_data[key]:
                        uuid_file = str(uuid1())
                        file_name, file_extension = os.path.splitext(item.filename)
                        with open(path_formatter(staticPath) + "/" + uuid_file + file_extension, "wb") as fwr:
                            fwr.write(item.value)
                            fwr.close()
                        temp.append(path_formatter(staticPath) + "/" + uuid_file + file_extension)
                    form22[key] = temp
                    
                elif post_data[key].value.isdigit():
                    form22[key] = int(post_data[key].value)
                elif isfloat(post_data[key].value):
                    form22[key] = float(post_data[key].value)
                elif isinstance(post_data[key].value, bytes):
                   
                    uuid_file = str(uuid1())
                    file_name, file_extension = os.path.splitext(post_data[key].filename)
                    form22[key] = [path_formatter(staticPath) + "/" + uuid_file + file_extension]
                    with open(path_formatter(staticPath) + "/" + uuid_file + file_extension, "wb") as fwr:
                        fwr.write(post_data[key].value)
                        fwr.close()
                else:
                    form22[key] = post_data[key].value

            form22["_id"] = str(uuid1())
            q = dataa[spl_path[i]].copy()
            q.append(form22)
            dataa[spl_path[i]] = q
            return dataa
        elif method == "DELETE":
            q = dataa[spl_path[i]].copy()
            
            fil_data = [obj for obj in q if str(obj[list(post_data.keys())[0]]) !=  post_data[list(post_data.keys())[0]]]
            dataa[spl_path[i]] = fil_data
            return dataa
        elif method == "PUT":
            q = dataa[spl_path[i]].copy()
            
            form22 = dict()

            for key in post_data["_user_put_data_"].keys():
                if isinstance(post_data["_user_put_data_"][key], list):
                    temp = list()
                    for item in post_data["_user_put_data_"][key]:
                        uuid_file = str(uuid1())
                        file_name, file_extension = os.path.splitext(item.filename)
                        with open(path_formatter(staticPath) + "/" + uuid_file + file_extension, "wb") as fwr:
                            fwr.write(item.value)
                            fwr.close()
                        temp.append(path_formatter(staticPath) + "/" + uuid_file + file_extension)
                    form22[key] = temp
                elif post_data["_user_put_data_"][key].value.isdigit():
                    form22[key] = int(post_data["_user_put_data_"][key].value)
                elif isfloat(post_data["_user_put_data_"][key].value):
                    form22[key] = float(post_data["_user_put_data_"][key].value)
                elif isinstance(post_data["_user_put_data_"][key].value, bytes):
                    uuid_file = str(uuid1())
                    file_name, file_extension = os.path.splitext(post_data["_user_put_data_"][key].filename)
                    form22[key] = [path_formatter(staticPath) + "/" + uuid_file + file_extension]
                    with open(path_formatter(staticPath) + "/" + uuid_file + file_extension, "wb") as fwr:
                        fwr.write(post_data["_user_put_data_"][key].value)
                        fwr.close()
                else:
                    form22[key] = post_data["_user_put_data_"][key].value

            for obj in q:
                if str(obj[list(post_data.keys())[1]]) == post_data[list(post_data.keys())[1]]:
                    for k, v in form22.items():
                        obj[k] = v

            dataa[spl_path[i]] = q
            return dataa
        
    else:
        s = dataa.copy()
        dataa[spl_path[i]] = props_getter(spl_path, i + 1, s[spl_path[i]], post_data, method)
        return dataa



class MyServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")        
        self.end_headers()
    
    def do_GET(self):
        try:
            p_url = urlparse(self.path)
            qs = parse_qs(p_url.query)
            ep_list = [x for x in endpoints if x["path"] == p_url.path]
            
            if(ep_list):
                ep_item = ep_list[0]
                f_json_file = open(path_formatter(jsonPath) + "/" + ep_item["json"], "r+")
                
                json_data = json.load(f_json_file)

                f_json_file.close()
                if qs.get("select"):
                    
                    for i in range(len(qs["select"][0].split("__"))):
                        
                        json_data = json_data[qs["select"][0].split("__")[i]]

                    for k, v in qs.items():
                        if k != "select":
                            json_data = [item for item in json_data if str(item[k]) == v[0]]
                            break
                    
                if isinstance(json_data, list):
                    json_data.reverse()
            
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
                
            else:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"message": f'Path {urlparse(self.path).path} is not set.'}), "utf-8"))
        except:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"message": "Error! Please check your arguments."}), "utf-8"))


    def do_POST(self):
        try:
        
            p_url = urlparse(self.path)
            qs = parse_qs(p_url.query)
            ep_list = [x for x in endpoints if x["path"] == p_url.path]
            
            if(ep_list):
                
                ep_item = ep_list[0]
                
                f_json_file = open(path_formatter(jsonPath) + "/" + ep_item["json"], "r+")
                json_data = json.load(f_json_file)
                f_json_file.close()

                spl_path = qs["select"][0].split("__")
                
                form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                })
                
                json_data = props_getter(spl_path, 0, json_data, form, "POST")

                f_json_file = open(path_formatter(jsonPath) + "/" + ep_item["json"], "w+")
                json.dump(json_data, f_json_file)
                f_json_file.close()

                for i in range(len(qs["select"][0].split("__"))):
                    json_data = json_data[qs["select"][0].split("__")[i]]

                json_data = json_data[::-1]

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
            
            else:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"message": f'Path {urlparse(self.path).path} is not set.'}), "utf-8"))
        except:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"message": "Error! Please check your arguments."}), "utf-8"))
    
    def do_PUT(self):
        try:           
            p_url = urlparse(self.path)
            qs = parse_qs(p_url.query)
            ep_list = [x for x in endpoints if x["path"] == p_url.path]
            
            if(ep_list):
                
                ep_item = ep_list[0]
            
                f_json_file = open(path_formatter(jsonPath) + "/" + ep_item["json"], "r+")
                
                json_data = json.load(f_json_file)
                f_json_file.close()
                
                spl_path = qs["select"][0].split("__")
            
                form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                })
    
                put_data2 = dict()
                put_data2['_user_put_data_'] = form
                
                
                for k, v in qs.items():
                    if(k != "select"):
                        put_data2[k] = v[0]
                        break
                
                json_data = props_getter(spl_path, 0, json_data, put_data2, "PUT")

                f_json_file = open(path_formatter(jsonPath) + "/" + ep_item["json"], "w+")
                json.dump(json_data, f_json_file)
                f_json_file.close()

                for i in range(len(qs["select"][0].split("__"))):
                    json_data = json_data[qs["select"][0].split("__")[i]]

                json_data = json_data[::-1]

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header('Access-Control-Allow-Origin', '*') 
                self.end_headers()
                
                self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
                
            else:
                self.send_response(400)
                
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"message": f'Path {urlparse(self.path).path} is not set.'}), "utf-8"))
        except:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"message": "Error! Please check your arguments."}), "utf-8"))
    

    def do_DELETE(self):    
        try:
            p_url = urlparse(self.path)
            qs = parse_qs(p_url.query)
            ep_list = [x for x in endpoints if x["path"] == p_url.path]
            
            if(ep_list):
                
                ep_item = ep_list[0]
                
                f_json_file = open(path_formatter(jsonPath) + "/" + ep_item["json"], "r+")
                
                json_data = json.load(f_json_file)
                f_json_file.close()
                
                # spl_len = len(spl_path)

                spl_path = qs["select"][0].split("__")
                del_par = dict()
                for k, v in qs.items():
                    if(k != "select"):
                        del_par[k] = v[0]
                        break
             
                json_data = props_getter(spl_path, 0, json_data, del_par, "DELETE")

                f_json_file = open(path_formatter(jsonPath) + "/" + ep_item["json"], "w+")
                json.dump(json_data, f_json_file)
                f_json_file.close()

                for i in range(len(qs["select"][0].split("__"))):
                    json_data = json_data[qs["select"][0].split("__")[i]]

                json_data = json_data[::-1]

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
                
            else:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
            
                self.wfile.write(bytes(json.dumps({"message": f'Path {urlparse(self.path).path} is not set.'}), "utf-8"))
        except:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"message": "Error! Please check your arguments."}), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")