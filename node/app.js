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

app.post('/stats-users',async (req,res)=>{
    data = await apiDict[req.session.user].getWholeThreadHistory(req.body.threadId);
    let response;
    try{
        response = await axios.post('http://python:8081/users_metrics',{
            'conversation': data
        });
    } catch(err) {
        console.log('Error while sending data',err);
    }
    data = response.data

    let dict_key = {};

    for(var i=0, c=data['sent messages'].length;i<c;i++){
        let message = data['sent messages'][i];
        if(dict_key[message[0]]){
            message[0] = dict_key[message[0]];
        } else{
            dict_key[message[0]] = (await apiDict[req.session.user].getUserInfo(message[0]))[message[0]].name;
            message[0] = dict_key[message[0]];
        }
        data['sent messages'][i] = message;
    }


    for(var i=0, c=data['received reactions'].length;i<c;i++){
        let message = data['received reactions'][i];
        if(dict_key[message[0]]){
            message[0] = dict_key[message[0]];
        } else{
            dict_key[message[0]] = (await apiDict[req.session.user].getUserInfo(message[0]))[message[0]].name;
            message[0] = dict_key[message[0]];
        }
        data['received reactions'][i] = message;
    }


    for(var i=0, c=data['graph_data'].nodes.length;i<c;i++){
        let message = data['graph_data'].nodes[i];
        if(dict_key[message['id']]){
            message['label'] = dict_key[message['id']];
        } else{
            let name = await apiDict[req.session.user].getUserInfo(message['id']);
            dict_key[message['id']] = name[message['id']].name;
            message['label'] = dict_key[message['id']];
        }
        data['graph_data'].nodes[i] = message;
    }

    for(var i=0, c=data['given reactions'].length;i<c;i++){
        let message = data['given reactions'][i];
        if(dict_key[message[0]]){
            message[0] = dict_key[message[0]];
        } else{
            dict_key[message[0]] = (await apiDict[req.session.user].getUserInfo(message[0]))[message[0]].name;
            message[0] = dict_key[message[0]];
        }
        data['given reactions'][i] = message;
    }

    res.render('threadStats.ejs',{'graph_data':data['graph_data'],'sent_messages':data['sent messages'],'given_reactions':data['given reactions'],'received_reactions':data['received reactions']});
});

app.post('/stats-messages',async (req,res)=>{
    data = await apiDict[req.session.user].getWholeThreadHistory(req.body.threadId);
    try{
        response = await axios.post('http://python:8081/messages_metrics',{
            'conversation': data
        });
    } catch(err) {
        console.log('Error while sending data',err);
    }
    data = response.data
    console.log(data);
    res.render('threadMessagesStats.ejs',{'data':data,'all':data['all'],'images':data['images']});
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
