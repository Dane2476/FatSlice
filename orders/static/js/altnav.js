document.addEventListener("scroll", function(){
  let nav = document.querySelector(".nav");
  if(window.scrollY > 1) {
    nav.style.backgroundColor = 'rgba(200,200,200,.7)';


  }
  else if (window.scrollY < 1){
    nav.style.backgroundColor = 'rgba(250, 250, 250, 1)';
  }

});
