document.addEventListener("DOMContentLoaded", function () {
  const divs = document.querySelectorAll("#editInput");
  console.log(divs.length);
  divs.forEach((element) => {
    const button = element.querySelector("#editInputButton");
    button.addEventListener("click", (event) => {
      event.preventDefault();

      button.style.display = "none";

      const editTextarea = document.createElement("textarea");
      editTextarea.rows = 3;
      editTextarea.cols = 50;
      editTextarea.required = true;
      editTextarea.name = "editedEntry";

      const br = document.createElement("br");

      const editSubmitButton = document.createElement("input");
      editSubmitButton.type = "submit";
      editSubmitButton.value = "Edit";

      const cancelButton = document.createElement("button");
      cancelButton.innerHTML = "Cancel";
      cancelButton.addEventListener("click", () => {
        document.querySelector("#editDiv").style.display = "none";
        document.querySelector("#editInput").style.display = "block";
      });

      element.appendChild(editTextarea);
      element.appendChild(br);
      element.appendChild(editSubmitButton);
      element.appendChild(cancelButton);
      
    });
  });

  // for (let i = 0; i < buttons.length; i++) {
  //   buttons[i].addEventListener("click", (event) => {
  //     event.preventDefault();
  //     editEntry();

  //   });
  // }
});

const editEntry = () => {
  document.querySelector("#editInput").style.display = "none";

  const editTextarea = document.createElement("textarea");
  editTextarea.rows = 3;
  editTextarea.cols = 50;
  editTextarea.name = "editedEntry";

  const br = document.createElement("br");

  const editSubmitButton = document.createElement("input");
  editSubmitButton.type = "submit";
  editSubmitButton.value = "Edit";

  document.querySelector("#editDiv").appendChild(editTextarea);
  document.querySelector("#editDiv").appendChild(br);
  document.querySelector("#editDiv").appendChild(editSubmitButton);
  document.querySelector("#editDiv").appendChild(cancelButton);
};
