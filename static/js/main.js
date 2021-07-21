document.addEventListener("click", function (argument){
 if(argument.target.classList.contains("gallery-item")||argument.target.classList.contains("cart-item-image")){
    const src = argument.target.getAttribute("src");
    document.querySelector(".modal-img").src = src;
    const myModal = new bootstrap.Modal(document.getElementById('gallery-modal'));
    myModal.show();
 }
});


