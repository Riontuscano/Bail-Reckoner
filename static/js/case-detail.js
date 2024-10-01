const menuicon = document.querySelector("#menu-icon");
const menu = document.querySelector(".block");
const menuclose = document.querySelector("#cancel");
const submenu = document.getElementById("subwrap");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-bar .step");
const progressLines = document.querySelectorAll(".progress-bar .line");
const mainform = document.querySelector("#multiStepForm");
const collsoc = document.getElementById('collectionsociety')

let formStepIndex = 0; 

// suggestion section pre defined



function toggleprofile() {
    submenu.classList.toggle("open-menu");

    window.onscroll = () =>{
     menu.classList.remove("open-menu");

    }
  }

function activateMenu() {
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

document.addEventListener('DOMContentLoaded', function() {
    const selectBtn = document.querySelector('.select-btn');
    const optionsContainer = document.querySelector('.options-container');
    const options = document.querySelectorAll('.option');
    const badgeContainer = document.querySelector('.badge-container');
    const arrow = document.querySelector('.arrow');
    
    let selectedOptions = new Set();
    
    selectBtn.addEventListener('click', () => {
      optionsContainer.style.display = 
        optionsContainer.style.display === 'block' ? 'none' : 'block';
      arrow.classList.toggle('up');
    });
    
    options.forEach(option => {
      option.addEventListener('click', () => {
        const value = option.dataset.value;
        const text = option.textContent;
        
        if (selectedOptions.has(value)) {
          selectedOptions.delete(value);
          option.classList.remove('selected');
          removeBadge(value);
        } else {
          selectedOptions.add(value);
          option.classList.add('selected');
          createBadge(value, text);
        }
      });
    });
    
    function createBadge(value, text) {
      const badge = document.createElement('div');
      badge.classList.add('badge');
      badge.dataset.value = value;
      badge.innerHTML = `
        ${text}
        <p class="remove-btn">&times;</p>
      `;
      
      badge.querySelector('.remove-btn').addEventListener('click', () => {
        selectedOptions.delete(value);
        const option = document.querySelector(`.option[data-value="${value}"]`);
        option.classList.remove('selected');
        removeBadge(value);
      });
      
      badgeContainer.appendChild(badge);
    }
    
    function removeBadge(value) {
      const badge = badgeContainer.querySelector(`.badge[data-value="${value}"]`);
      if (badge) {
        badge.remove();
      }
    }
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!selectBtn.contains(e.target) && !optionsContainer.contains(e.target)) {
        optionsContainer.style.display = 'none';
        arrow.classList.remove('up');
      }
    });
  });

document.querySelectorAll(".next-btn").forEach((button) => {
  button.addEventListener("click", () => {
    if (formStepIndex < formSteps.length - 1) {  
      formStepIndex++;
      updateFormSteps();
      updateProgressBar();
    }
  });
});

// Handle 'Previous' button click event
document.querySelectorAll(".prev-btn").forEach((button) => {
  button.addEventListener("click", () => {
    if (formStepIndex > 0) {  
      formStepIndex--;
      updateFormSteps();
      updateProgressBar();
    }
  });
});

// Update form steps based on the current index
function updateFormSteps() {
  formSteps.forEach((formStep, index) => {
    formStep.classList.toggle("active", index === formStepIndex);
  });
}

// Update the progress bar to highlight current step and completed steps
function updateProgressBar() {
  progressSteps.forEach((progressStep, index) => {
    if (index <= formStepIndex) {
      progressStep.classList.add("active");
    } else {
      progressStep.classList.remove("active");
    }
  });

  progressLines.forEach((line, index) => {
    if (index < formStepIndex) {
      line.classList.add("active");
    } else {
      line.classList.remove("active");
    }
  });
}

// Form submission logic
document.getElementById("multiStepForm").addEventListener("submit", function(event) {
  //Uncomment the following line if you want to handle form submission with JavaScript (e.g., via AJAX)
  // event.preventDefault();

  // For actual submission, comment out the alert and allow default behavior
  // alert("Form Submitted!");

  // If using AJAX, uncomment the following code:
  
  event.preventDefault(); // Prevent default form submission

  // Create a FormData object
  const formData = new FormData(this);

  // Send the data using Fetch API
  fetch(this.action, {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(result => {
    console.log(result); // Handle the response
    alert("Form Submitted!");
    mainform.reset();
    
  })
  .catch(error => console.error('Error:', error));
  
});


// suggestin section
// let sorted_cs = collectionsocieties.sort();
// collsoc.addEventListener("keyup", (e) => {
//   removeElement();
//   for (let i of sorted_cs) {
    
//       if(i.toLowerCase().startsWith(collsoc.value.toLowerCase()) && collsoc.value != ""){
//           let listItem = document.createElement("li");

//           listItem.classList.add("list-items");
//           listItem.style.cursor = "pointer";
//           listItem.setAttribute("onclick","displayNames('"+ i +"')");

//           let word = "<b>" + i.substring(0,collsoc.value.length) + "</b>";
//           word += i.substring(collsoc.value.length);
          
//           listItem.innerHTML = word;
//           document.querySelector(".societysuggest").appendChild(listItem);
//       }
//   }
// });



// function displayNames(value) {
//   collsoc.value = value;
//   removeElement();
// }

// function removeElement(){
//   let delitem = document.querySelectorAll(".list-items");
//   delitem.forEach((item) =>{
//     item.remove();
//   });
// }
activateMenu();
