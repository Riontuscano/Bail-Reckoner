const menuicon = document.querySelector("#menu-icon");
const menu = document.querySelector(".block");
const menuclose = document.querySelector("#cancel");
const submenu = document.getElementById("subwrap");


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


activateMenu()