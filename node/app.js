const express = require('express');
const http = require('http');
const fs = require('fs');
const bodyParser = require('body-parser');
const ApiListener = require('./apiManager');
const cookieSession = require('cookie-session');
const axios = require('axios');

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
    keys: ['key1','key2'],
}));

app.get('/start',(req,res)=>{
    if(req.session.user){
        req.session.user = undefined;
    }
    res.redirect('/');
})

app.get('/',async (req,res)=>{
    if(req.session.user){
        threadList = await apiDict[req.session.user].getThreadList();
        res.render('index',{'user':req.session.user,'listThread':threadList});
    } else{
        res.render('index');
    }
});

app.get('/deconnect',(req,res)=>{
    if(req.session.user){
        req.session.user = undefined;
        res.redirect('/');
    }
    else{
        res.redirect('/');
    }
});

app.post('/stats',async (req,res)=>{
    data = await apiDict[req.session.user].getWholeThreadHistory(req.body.threadId);
    let response;
    try{
        response = await axios.post('http://localhost:8081/raw_conversation',{
            'conversation': data
        });
        console.log(response);
    } catch(err) {
        console.log('Error while sending data',err);
    }
    res.render('threadStats.ejs')
});

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
