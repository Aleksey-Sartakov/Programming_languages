const express = require("express");
const fs = require("fs");

const app = express();
const jsonParser = express.json();

app.use(express.static(__dirname + "/public"));

app.post("/api/dirpath", jsonParser, function(request, response){
    if(!request.body) return res.sendStatus(400);

    const path = request.body.path;

    fs.readdir(path,(err, files) => 
    {
        if(err)
        {
            console.log(err);
            response.send(JSON.stringify({data: err}));
            return;
        }
        
        response.send(files);
    });
    
});

app.post("/api/download", jsonParser, function(request, response){
    if(!request.body) return res.sendStatus(400);

    const path = request.body.path;

    response.download(path)
    
});

app.listen(3000);
