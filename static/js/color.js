const arrColor = [];

document.addEventListener("click", function eventHandler(e){
    if(e !== null){
        let getColor = document.querySelector('#exampleColorInput').value;
        arrColor.push(getColor);
        console.log(arrColor[0]);
    }
});


