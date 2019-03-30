const express = require('express');
const http = require('http');
const credentials = require('./login');
const fs = require('fs');

let apiDict = {},

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

let api;

async function fetchHistory(){
    try{
        data = await apiListener.getWholeThreadHistory('2085660434838292');
        fs.writeFile('data.json',JSON.stringify(data),(err)=>{
            if(err){
                console.log('error while writing');
            }
        });
    } catch(err) {
        console.log('Error while fetching history',err);
    }
}

async function loginFunction(email,password){
    try{
        const apiListener = new ApiListener();
        return await ApiListener.init(email,password);
    } catch (err) {
        console.log('Error while login',err);
        throw Error('Error while login');
    }
}

loginFunction();

app.get('localhost:3000/login',async (res,req)=>{
    apiDict[req.params.email] = await loginFunction(req.params.email,req.params.password);
    res.send(200);
});