document.addEventListener("click", function (argument){
 if(argument.target.classList.contains("gallery-item")||argument.target.classList.contains("cart-item-image")){
    const src = argument.target.getAttribute("src");
    document.querySelector(".modal-img").src = src;
    const myModal = new bootstrap.Modal(document.getElementById('gallery-modal'));
    myModal.show();
 }
});


const modal = document.getElementById("myModal");
const modal1 = document.getElementById("myModal1");
const modal2 = document.getElementById("myModal2");
const modal3 = document.getElementById("myModal3");


const btn = document.getElementById("myBtn");
const btn1 = document.getElementById("myBtn1");
const btn2 = document.getElementById("myBtn2");
const btn3 = document.getElementById("myBtn3");


const span = document.getElementsByClassName("close")[0];


btn.onclick = function() {
  modal.style.display = "block";
}

btn1.onclick = function() {
  modal1.style.display = "block";
}

btn2.onclick = function() {
  modal2.style.display = "block";
}

btn3.onclick = function() {
  modal3.style.display = "block";
}


span.onclick = function() {
  modal.style.display = "none";
  modal1.style.display = "none";
  modal2.style.display = "none";
  modal3.style.display = "none";
}


window.onclick = function(event) {
  if (event.target == modal || event.target == modal1 || event.target == modal2 || event.target == modal3) {
    modal.style.display = "none";
    modal1.style.display = "none";
    modal2.style.display = "none";
    modal3.style.display = "none";
  }
}


