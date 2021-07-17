document.addEventListener("click", function (argument){
 if(argument.target.classList.contains("gallery-item")||argument.target.classList.contains("cart-item-image")){
    const src = argument.target.getAttribute("src");
    document.querySelector(".modal-img").src = src;
    const myModal = new bootstrap.Modal(document.getElementById('gallery-modal'));
    myModal.show();
 }
})

const arrColor = []

document.addEventListener("click", function(e){
    if(e !== null){
        let getColor = document.querySelector('#exampleColorInput');
        let arrColor = [getColor.value];
        console.log(arrColor[0]);
    }
})
document.querySelector('.change-color').style['background-color']= arrColor[0];



