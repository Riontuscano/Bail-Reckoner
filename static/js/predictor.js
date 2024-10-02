const menuicon = document.querySelector("#menu-icon");
const menu = document.querySelector(".block");
const menuclose = document.querySelector("#cancel");
const submenu = document.getElementById("subwrap");
const progressValueElement = document.querySelector('.progress-value');
const progressCircleElement = document.querySelector('.progress-circle::after');
const slider = document.getElementById('percentageSlider');
    
const fill = document.querySelector('.fill');
    const percentageText = document.querySelector('.percentage-text');

    function updatePercentage() {
      const value = slider.value;
      fill.style.height = `${value}%`;
      percentageText.textContent = `${value}%`;
    }

    slider.addEventListener('input', updatePercentage);

function toggleprofile() {
    submenu.classList.toggle("open-menu");

    window.onscroll = () =>{
     menu.classList.remove("open-menu");

    }
  }

function activateMenu() {
    // console.log("Hello")
  menuicon.onclick = () => {
    menu.classList.add("active");
    
  };
  
  menuclose.onclick = () => {
    menu.classList.remove("active");
  };
  
  window.onscroll = () => {
    menu.classList.remove("active");
  };
}
// function updateProgressBar(percentage) {
//   const progressValueElement = document.querySelector('.progress-value');
//   const progressCircleElement = document.querySelector('.progress-circle::after');

//   progressValueElement.textContent = percentage + '%';
//   progressCircleElement.style.transform = `rotate(${percentage * 3.6}deg)`;
// }

// updateProgressBar(75); 

updateProgressBar(75); 
activateMenu()