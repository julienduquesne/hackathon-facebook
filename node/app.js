const express = require('express');
const http = require('http');
const fs = require('fs');
const bodyParser = require('body-parser');
const ApiListener = require('./apiManager');
const cookieSession = require('cookie-session');

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

app.use(cookieSession({
    name:'session',
    keys: ['key1','key2']
}));

app.get('/',async (req,res)=>{
    if(req.session.user){
        threadList = await apiDict[req.session.user].getThreadList();
        res.render('index',{'user':req.session.user,'listThread':threadList});
    } else{
        res.render('index');
    }
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
        await apiListener.init(email,password);
        return apiListener
    } catch (err) {
        console.log('Error while login',err);
        throw Error('Error while login');
    }
}

app.post('/login',async (request,response)=>{
    let threadList;
    try{
        apiDict[request.body.email] = await loginFunction(request.body.email,request.body.password);
        request.session.user = request.body.email;
    } catch(err){
        console.log(err)
        return;
    }
    response.redirect('/');
});

