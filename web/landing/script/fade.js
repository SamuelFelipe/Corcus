const slider = document.getElementById('list');/* ul element */


/* -----------------------peticion de las imagenes----------------------------- */
let xhr;
let interval = 0;


const buttonL = document.getElementById('buttonL');
const buttonR = document.getElementById('buttonR');

if(window.XMLHttpRequest) xhr = new XMLHttpRequest();
else  xhr = new ActiveXObject("Microsoft.XMLHTTP");

xhr.open('GET', '../images/images.json');

const datos = xhr.addEventListener('load', (data)=>{
    JSONData = JSON.parse(data.target.response);
    console.log(JSONData);
    displayImages(JSONData);
    interactive();
});

xhr.send();

function interactive(){
    console.log(slider)
    
    let cont = slider.children.length-1;
    function startInterval() { interval= setInterval(counter, 5000);}

    startInterval();

    function counter(){
        // console.log('from timer')
        cont--;
        if(cont < 0)  cont = slider.children.length-1; 
        transition();
    }
    
    function transition(){
        // if(cont < 0) cont = 0;
        // else if(cont > (slider.children.length-1)) cont--;
        // slider.style.marginLeft = `-${cont}00%`;
        console.log(cont)
        if(slider.children[cont].style.opacity == 1) slider.children[cont+1].setAttribute('style', 'opacity: 0;');
        else slider.children[cont].setAttribute('style', 'opacity: 1;');

        console.log(slider.children[cont].style.opacity)
    }
}

function displayImages(x){
    const frag = document.createDocumentFragment();

    slider.setAttribute("style", `width: 100%`);

    for(const images of x){
        const itemLI = document.createElement('LI');
        const picture = document.createElement('IMG');

        picture.setAttribute('src', `${images.imageLocation}`);
        picture.setAttribute('class', `back-images `);
    
        itemLI.setAttribute('position', 'absolute');
        itemLI.setAttribute('style', 'opacity: 1');
        // itemLI.setAttribute('id', `images-${images.id}`)

        itemLI.appendChild(picture);
        frag.insertBefore(itemLI, frag.children[0]);
    }
    slider.appendChild(frag);
}
