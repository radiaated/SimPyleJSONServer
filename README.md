# SimPyle JSON Server 0.0.1
SimPyle JSON Server lets you host a local server which is capable of serving HTTP requests. As of now, it supports `GET`, `POST`, `PUT` and `DELETE` method.
Recommended: Python3
___
### Setup

Git Clone this repo.

##### Folder Structure
- json (add all the json files here)
- static (all the uploaded files go here)

##### Commands

At the root directory, run the command to run the server.
```
python server.py
```

Map the url path to json file

```
python server.py path=/products json=products.json
```

Run the server on the port.
```
python server.py port=8080
```

Change the path to the folder where all the JSON files lie.
```
python server.py json_path=/jsonNew
```

Change the path to the folder where all the uploaded files go.
```
python server.py static_path=/staticNew
```

View all the url paths
```
python server.py view
```

___




#### URL Pattern

`
http://localhost:<port>/<path>?select=<json_array>&<payload_key>=<payload_value>
`
#### JSON Format
JSON must be **Object** type which contains your main data.
Preparing JSON
``` json
{
  "version": 1,
  "products": {
    "section": "Electronics",
    "productsList": [
      {
        "_id": "6b114602-efe1-11ed-a6b7-204747521540",
        "name": "Sony PlayStation 5",
        "description": "The Sony PlayStation 5 is the latest gaming console from Sony.",
        "price": 499.99,
        "category": "Gaming"
      },
      {
        "_id": "6b12059d-efe1-11ed-b3f0-204747521540",
        "name": "Apple iPhone 13",
        "description": "The Apple iPhone 13 is the latest smartphone from Apple.",
        "price": 799.99,
        "category": "Electronics"
      }
    ]
  }
}
```

___
#### GET
With GET method, receive whole data of JSON file in body of the response.
```
http://localhost:8080/products
```

You can go through the object to receive only certain value of JSON object by passing query strings to URL

```
http://localhost:8080/products?select=products__productsList
```

Filter the selected array of objects by passing the existing key/value of the objects in the query string of url.
```
http://localhost:8080/products?select=products__productsList&_id=6b114602-efe1-11ed-a6b7-204747521540
```

Above URL returns the array of objects **productsList** from **{products.productsList}** of the JSON object.
> Note: **"__"** double underscore allows to expand only objects 
___

#### POST
POST method supports inserting an object into an array of objects in JSON.
Via POST, the new inserted object is assigned a key **_id** with unqiue ID value.
There is no support for payload data validation like in Database.
It is mandatory to select the key of JSON object where your array lies by using query string **select**

```
http://localhost:8080/products?select=products__productsList
```

The payload needs to be appended to the request body of the HTTP request

`POST /products?select=products__productsList HTTP/1.1`
`Host: localhost:8080`
`Content-Type: multipart/form-data; boundary=----WebKitFormBoundary<>`
`----WebKitFormBoundary<>`
`Content-Disposition: form-data; name="name"`
`Sony WH-1000XM4
----WebKitFormBoundary<>`
`Content-Disposition: form-data; name="description"`
`The Sony WH-1000XM4 is a premium noise-cancelling headphone with high-quality sound and long battery life. ----WebKitFormBoundary<> 
...`
___

#### PUT
PUT method supports updating objects into an array of objects in JSON.
There is no support for payload data validation like in Database.
It is mandatory to select the key of JSON object where your array lies by using query string **select**.
The key/value of the object which to be updated must be passed in query string.  
```
http://localhost:8080/products?select=products__productsList&_id=6b114602-efe1-11ed-a6b7-204747521540
```

The payload needs to be appended to the request body of the HTTP request. The payload can contain multiple information.

`PUT /products?products?select=products__productsList&_id=6b114602-efe1-11ed-a6b7-204747521540 HTTP/1.1`
`Host: localhost:8080`
`Content-Type: multipart/form-data; boundary=----WebKitFormBoundary<>`
`----WebKitFormBoundary<>`
`Content-Disposition: form-data; name="name"`
`PlayStation 5 Console
----WebKitFormBoundary<>`
`Content-Disposition: form-data; name="description"`
`The Sony PlayStation 5 Console is the latest gaming console from Sony. ----WebKitFormBoundary<> 
...`

___
#### DELETE
PUT method supports deleting the object of an array in JSON. 
It is mandatory to select the key where your array lies using query string **select**.
The key/value of the object which to be updated must be passed in query string. 
```
http://localhost:8080/products?select=products__productsList&_id=6b114602-efe1-11ed-a6b7-204747521540
```

___

## Handling Client Side (Javascript)

#### GET

```JS
fetch(
    "http://localhost:8080/products?select=products__productsList", {
        method: "GET",
    }
);
```

#### POST
Initialize an object of FormData and append it to the body of HTTP request
```JS
let fd = new FormData();
fd.append("name", "Sony WH-1000XM4");
fd.append(
    "description",
    "The Sony WH-1000XM4 is a premium noise-cancelling headphone with high-quality sound and long battery life."
);
fd.append("price", 349.99);
fd.append("category", "Headphones");


fetch(
    "http://localhost:8080/products?select=products__productsList", {
        method: "POST",
        body: fd,
    }
);
```

#### PUT
Initialize an object of FormData and append it to the body of HTTP request
```JS
var fd = new FormData();
fd.append("name", "Sony WH-1000XM3");
fd.append(
    "description",
    "The predecessor to the WH-1000XM4, these noise-canceling headphones are still a popular choice thanks to their excellent sound quality and noise-canceling capabilities."
);

fetch(
    "http://localhost:8080/products?select=products__productsList&_id=2e6bcbe1-eff0-11ed-935d-204747521540", {
        method: "PUT",
        body: fd,
    }
);
```

#### DELETE

``` js
fetch(
    "http://localhost:8080/products?select=products__productsList&_id=6b12059d-efe1-11ed-b3f0-204747521540", {
        method: "DELETE",
    }
);
```

#### Uploading Files in JS
To upload a single file, append a **File** object to **FormData**
``` js
const inputFieldFile = document.getElementById("input_field_file").files;

let fd = new FormData();

fd.append("product_image", inputFieldFile[0]);
```

To upload a multiple files, append the **File** objects to **FormData** using loop
``` js
const inputFieldFile = document.getElementById("input_field_file").files;

for (let file of inputFieldFile) {
  console.log(file);
  fd.append("product_image", file);
}
```

###### Don't mind the untidy code. 

##### THE END
###### HAPPY HACKING!