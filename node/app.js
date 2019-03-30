const express = require('express');
const http = require('http');
const fs = require('fs');
const bodyParser = require('body-parser');
const ApiListener = require('./apiManager');

let apiDict = {},

app = express();

server = http.createServer(app);
server.listen(3000,()=>{
    console.log('Listening');
});

app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/static/'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());

app.get('/',(req,res)=>{
    res.render('index');
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
        return await apiListener.init(email,password);
    } catch (err) {
        console.log('Error while login',err);
        throw Error('Error while login');
    }
}

app.post('/login',async (request,response)=>{
    try{
        apiDict[request.body.email] = await loginFunction(request.body.email,request.body.password);
    } catch(err){
        console.log(err)
        return;
    }
    response.render('index',{'user':request.body.email});
});

