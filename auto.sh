#!/usr/bin/env bash

curl -i -X POST -H "Content-Type: application/json" -d '{"company":"evo","username":"samu","password":"1234abc"}' http://127.0.0.1:5000/api/signup >> /dev/null
curl -i -u samu:1234abc -X POST -H "Content-Type: application/json" -d '{"no_acount":"341412022993","names":"Felipe","forenames":"Sierra","c_type":"Termino Indefinido","id":"101","position":"Oficina","eps":"Famisanar"}' http://127.0.0.1:5000/api/employees >> /dev/null
curl -i -u samu:1234abc -X POST -H "Content-Type: application/json" -d '{"no_acount":"341412022113","names":"Samuel","forenames":"Correa","c_type":"Termino Indefinido","id":"100","position":"Oficina","eps":"Famisanar"}' http://127.0.0.1:5000/api/employees >> /dev/null
curl -i -u samu:1234abc -X POST -H "Content-Type: application/json" -d '{"no_acount":"341412001223","names":"Jesus","forenames":"Correa","c_type":"Termino Indefinido","id":"102","position":"algo","eps":"Salud Total"}' http://127.0.0.1:5000/api/employees >> /dev/null
curl -i -u samu:1234abc -X GET http://127.0.0.1:5000/api/employees
