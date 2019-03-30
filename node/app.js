const express = require('express');
const http = require('http');

app = express();

server = http.createServer(app);
server.listen(3000,()=>{
    console.log('Listening');
});

app.get('/',(req,res)=>{
    res.status(200).send({
        msg:'Everything is working fine'
    })
});