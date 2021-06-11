/*      <li><img src="https://www.wallpapertip.com/wmimgs/4-41454_free-download-wallpapers-hd-space-wallpaper-hd-pc.jpg" alt="" class="back-images"></li>

                    <li><img src="https://cdn.wallpapersafari.com/3/74/iVxWUY.jpg" alt="" class="back-images"></li>

                    <li><img src="https://fondosmil.com/fondo/17060.jpg" alt="" class="back-images"></li> */



const slider = document.getElementById('list');

/* -----------------------peticion de las imagenes----------------------------- */
let xhr;
let cont = 0;
let interval = 0;


const buttonL = document.getElementById('buttonL');
const buttonR = document.getElementById('buttonR');


if(window.XMLHttpRequest) xhr = new XMLHttpRequest();
else  xhr = new ActiveXObject("Microsoft.XMLHTTP");



xhr.open('GET', '../images/images.json');


xhr.addEventListener('load', (data)=>{
    JSONData = JSON.parse(data.target.response);
    console.log(JSONData);
    displayImages(JSONData);
    const s = document.createElement('script');
    s.src = "../script/screenInfo.js"
    document.body.insertAdjacentElement('beforeend', s);
    interactive();
});

xhr.send();


function interactive(){

    function startInterval() { interval= setInterval(counter, 5000);}

    startInterval();

    /* ---------------------buttons---------------------------- */


  buttonL.addEventListener('click', ()=>{
        clearInterval(interval);
        // console.log('from buttom')
        cont--;
        transition();
        startInterval();
    })

    buttonR.addEventListener('click', ()=>{
        clearInterval(interval)
        // console.log('from buttom')
        cont++;
        transition();
        startInterval();
    })



    function counter(){
        // console.log('from timer')
        cont++;
        if(cont > (slider.children.length-1)) cont = 0;
        transition();
    }

    function transition(){
        if(cont < 0) cont = 0;
        else if(cont > (slider.children.length-1)) cont--;
        slider.style.marginLeft = `-${cont}00%`
        // console.log(cont);
    }
}




function displayImages(x){
    const frag = document.createDocumentFragment();

    for(const images of x){
        const itemLI = document.createElement('LI');
        const picture = document.createElement('IMG');

        picture.setAttribute('src', `${images.imageLocation}`);
        picture.setAttribute('class', `back-images image-${images.id}`);

        itemLI.setAttribute('class', 'li')
        itemLI.appendChild(picture);
        frag.appendChild(itemLI);
    }
    slider.appendChild(frag);

    const width = slider.children.length;

    slider.setAttribute("style", `width: ${width}00%`);
}









