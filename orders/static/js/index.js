
document.addEventListener("scroll", function(){
  if(window.scrollY > 300) {
    document.querySelector(".stickynav").style.top = '0';

  }
  else if (window.scrollY < 300){
    document.querySelector(".stickynav").style.top = '-80px';
  }

});
