
/* 

            <div class="aling-info"><div class="info"><h2>Lorem, ipsum dolor.</h2><div class="line"></div><p>Lorem ipsum dolor sit amet consectetur adipisicing elit. At, vel!</p></div></div>
*/

const list = document.getElementById('list');

if(window.XMLHttpRequest) xhr = new XMLHttpRequest();
else  xhr = new ActiveXObject("Microsoft.XMLHTTP");



xhr.open('GET', '../images/images.json');


xhr.addEventListener('load', (data)=>{
    const dataJSON = JSON.parse(data.target.response);
    setInfo(dataJSON);

});


xhr.send();

function setInfo(x){
    for(const dat in x){
        const container = document.createElement('div');
        container.className = 'aling-info';

        container.innerHTML = `<div class="info"><h2>${x[dat].info.title}</h2><div class="line"></div><p>${x[dat].info.comment}</p></div>`

        list.children[dat].appendChild(container);
    }
}