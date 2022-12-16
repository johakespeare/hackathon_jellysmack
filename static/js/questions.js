const slidesContainer = document.getElementById("slides-container");
const slide = document.querySelector(".slide");
const nextButton = document.getElementById("slide-arrow-next");
var nombreClics = 0;

nextButton.addEventListener("click", () => {
    nombreClics++;
  const slideWidth = slide.clientWidth;
  slidesContainer.scrollLeft += slideWidth;
  if(nombreClics==3){
    let btn = document.createElement("button");
    btn.innerHTML = "GO &#8250;";
    btn.className = "btnHome";
    btn.onclick = function(){send();};
    document.body.appendChild(btn);
    var element = document.getElementById("slide-arrow-next");
    element.remove();
  }
});

