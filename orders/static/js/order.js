let limit = 0;
let price = 0;

document.addEventListener("DOMContentLoaded", function(){
  // When a radio is selected, allow or disable checks depending on topping amt selected
  document.querySelectorAll('input[type="radio"]').forEach(function(radio){
    radio.addEventListener("change", updateLimit);
  });
  // Disable/enable checks depending on user topping amount selection
  document.querySelectorAll('input[type="checkbox"]').forEach(function(box){
    box.addEventListener("change", updateChecks);
  });
  // When a new section is opened, uncheck all boxes;
  document.querySelectorAll('.category').forEach(function(button){
    button.addEventListener("click", purgeChecks);
  })

});

function updateLimit(){
  document.querySelectorAll('input[type="radio"]').forEach(function(radio){
    if(radio.checked === true){
      limit = radio.value;
    }
  });
  updateChecks()
}

function updateChecks(){
  var checked = document.querySelectorAll('input[type="checkbox"]:checked');
  var unchecked = document.querySelectorAll('input[type="checkbox"]:not(:checked)');
  var allBoxes = document.querySelectorAll('input[type="checkbox"]');
  if(checked.length == limit){
    unchecked.forEach(function(unchecked){
      unchecked.disabled = true;
    });
  }
  else if (checked.length < limit){
    unchecked.forEach(function(unchecked){
      unchecked.disabled = false;
    });
  }
  else if (checked.length > limit){
    checked.forEach(function(checked){
      checked.checked = false;
    });
    if(limit>0){
      allBoxes.forEach(function(allBoxes){
        allBoxes.disabled = false;
      });
    }
    else{
      allBoxes.forEach(function(allBoxes){
        allBoxes.disabled = true;
      });
    }
  }
}

function purgeChecks(){
  // We want the user to be able to select sub toppings even though there aren't radios
  if(this.classList.contains("subs")){
    document.querySelectorAll('input[type="checkbox"]').forEach(function(box){
      box.checked = false;
      box.disabled = false;
      limit = 4;
    });
  }
  else{
    document.querySelectorAll('input[type="checkbox"]').forEach(function(box){
      box.checked = false;
      box.disabled = true;
    });
    document.querySelectorAll('input[type="radio"]').forEach(function(radio){
      radio.checked = false;
    });
    limit = 0;
  }

}
