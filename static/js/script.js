const counterElement = document.querySelector(".counter");
const barElements = document.querySelector(".bar");
const page1Content = document.querySelector(".page1content");
const cursor = document.querySelector(".cursor");
const menuicon = document.querySelector("#menu-icon");
const menu = document.querySelector(".block");
const menuclose = document.querySelector("#cancel");
const submenu = document.getElementById("subwrap");
const audiolist = document.querySelector(".song-container");
const musicfunc = document.querySelector('#play-pause');
const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatcontainer = document.querySelector(".chat-container");
const cart = document.querySelector(".cart");
const chatclose = document.querySelector("#close-cart");
const chatopen = document.querySelector("#menu-search");
let userText = null;



function toggleprofile() {
  submenu.classList.toggle("open-menu");
}
function cursorEffect() {
  page1Content.addEventListener("mousemove", function (e) {
    gsap.to(".cursor", {
      x: e.x,
      y: e.y,
    });
  });

  page1Content.addEventListener("mouseenter", function (e) {
    gsap.to(".cursor", {
      scale: 1,
      opacity: 1,
    });
  });
  page1Content.addEventListener("mouseleave", function (e) {
    gsap.to(".cursor", {
      scale: 0,
      opacity: 0,
    });
  });
}
function loadingCounter() {
  let currentValue = 0;

  function updateCounter() {
    if (currentValue === 100) {
      return;
    }
    currentValue += Math.floor(Math.random() * 10) + 1;

    if (currentValue > 100) {
      currentValue = 100;
    }

    counterElement.textContent = currentValue;
  }
  var delay = Math.floor(Math.random() * 250) + 10;
  setInterval(updateCounter, delay);
  gsap.to(".counter", 0.25, {
    delay: 2.5,
    opacity: 0,
  });

  gsap.to(".bar", 1.5, {
    delay: 2.5,
    height: 0,
    stagger: {
      amount: 0.5,
    },
    ease: "power4.inOut",
  });
}
function enableMain() {
  page1Content.style.zIndex = 16;
}
function scrollAnim() {
  gsap.registerPlugin(ScrollTrigger);

  // Using Locomotive Scroll from Locomotive https://github.com/locomotivemtl/locomotive-scroll

  const locoScroll = new LocomotiveScroll({
    el: document.querySelector("#main"),
    smooth: true,
  });
  // each time Locomotive Scroll updates, tell ScrollTrigger to update too (sync positioning)
  locoScroll.on("scroll", ScrollTrigger.update);

  // tell ScrollTrigger to use these proxy methods for the "#main" element since Locomotive Scroll is hijacking things
  ScrollTrigger.scrollerProxy("#main", {
    scrollTop(value) {
      return arguments.length
        ? locoScroll.scrollTo(value, 0, 0)
        : locoScroll.scroll.instance.scroll.y;
    }, // we don't have to define a scrollLeft because we're only scrolling vertically.
    getBoundingClientRect() {
      return {
        top: 0,
        left: 0,
        width: window.innerWidth,
        height: window.innerHeight,
      };
    },
    // LocomotiveScroll handles things completely differently on mobile devices - it doesn't even transform the container at all! So to get the correct behavior and avoid jitters, we should pin things with position: fixed on mobile. We sense it by checking to see if there's a transform applied to the container (the LocomotiveScroll-controlled element).
    pinType: document.querySelector("#main").style.transform
      ? "transform"
      : "fixed",
  });

  // each time the window updates, we should refresh ScrollTrigger and then update LocomotiveScroll.
  ScrollTrigger.addEventListener("refresh", () => locoScroll.update());

  // after everything is set up, refresh() ScrollTrigger and update LocomotiveScroll because padding may have been added for pinning, etc.
  ScrollTrigger.refresh();
}
function activatemenu() {
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

function toggleChat(){
  chatopen.onclick = () => {
    cart.classList.add("active");
  };
  chatclose.onclick = () => {
    cart.classList.remove("active");
  };

  window.onscroll = () => {
    cart.classList.remove("active");
  };
}






const createElement =(html,className) => {
  const chatDiv = document.createElement("div");
  chatDiv.classList.add("chat",className);
  chatDiv.innerHTML = html;
  return chatDiv;
};

const showtypingdot = () => {
  const html=`  <div class="chat-content">
                <div class="chat-details">
                  <img src="{{ url_for('static', filename='img/law-logo-rev.png') }}" alt="sys-img">
                <div class="typing-animation">
                  <div class="typing-dot"style="--delay:0.2s"></div>
                  <div class="typing-dot"style="--delay:0.3s"></div>
                  <div class="typing-dot"style="--delay:0.4s"></div>
                </div>
                </div>
              </div>`
  const outgoingChatDiv = createElement(html,"incoming")
  chatcontainer.appendChild(outgoingChatDiv);
  getChatResponse();
}
const handleOutgoingChat = () => {
  userText= chatInput.value.trim();
  // console.log(userText);
  const html=`<div class="chat-content">
              <div class="chat-details">
              <img src="{{ url_for('static', filename='img/lawyer1.jpeg') }}" alt="user-img">
              <p>${userText}</p>
              </div>
            </div>`
  const outgoingChatDiv = createElement(html,"outgoing")
  chatcontainer.appendChild(outgoingChatDiv);
  chatInput.value = "";
  setTimeout(showtypingdot,500);
}

sendButton.addEventListener("click",handleOutgoingChat);
const API_KEY = "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"

const getChatResponse = async () => {
  const API_URL = " https://api.openai.com/v1/completions";

  const requestOptions ={
    method:"POST",
    headers:{
      "Content-Type": "application/json",
      "Authorization": `Bearer ${API_KEY}`
    },
    body:JSON.stringify(
      {
        model: "gpt-3.5-turbo",
        prompt: userText,
        max_tokens: 2048,
        temperature: 0.2,
        top_p:1,
        n:1,
        stop: null
      }
    )
  }
  try{
    const response= await(await fetch(API_URL,requestOptions)).JSON();
    console.log(response);
  }catch(err){
    console.log(err);
  }
}
 
// scrollAnim();
setTimeout(enableMain, 5000);
loadingCounter();
cursorEffect();
activatemenu();
toggleChat();
