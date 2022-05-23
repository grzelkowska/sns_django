document.addEventListener("DOMContentLoaded", function () {
  const divs = document.querySelectorAll("#editInput");
  // console.log(divs.length);
  divs.forEach((element) => {
    // const entry = element.querySelector("p").innerHTML
    // console.log(entry)

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
      cancelButton.formNoValidate = true;

      element.appendChild(editTextarea);
      element.appendChild(br);
      element.appendChild(editSubmitButton);
      element.appendChild(cancelButton);

      cancelButton.addEventListener("click", (event) => {
        event.preventDefault();
        button.style.display = "block";
        // element.style.display = "none";
        editTextarea.style.display = "none";
        br.style.display = "none";
        editSubmitButton.style.display = "none";
        cancelButton.style.display = "none";
      });
    });
  });
});

const like = async (post_id) => {
  
  await fetch("/like_entry", {
    method: "POST",
    // credentials: "same-origin",
    // headers: {
    //   Accept: "application/json",
    //   "Content-Type": "application/json",
    //   "X-CSRFToken": document.forms[0].querySelector(
    //     'input[name="csrfmiddlewaretoken"]'
    //   ).value,
    // },
    body: JSON.stringify({
      user_id: user_id,
      post_id: post_id,
    }),
  });

  if (document.querySelector(`#p${post_id}`).value == "False") {
    document.querySelector(`#p${post_id}`).value = "True";
    document.querySelector(`#i${post_id}`).classList.remove('fa-regular')
    document.querySelector(`#i${post_id}`).classList.add('fa-solid')
    document.querySelector(`#s${post_id}`).innerHTML++
  } else {
    document.querySelector(`#p${post_id}`).value = "False";
    document.querySelector(`#i${post_id}`).classList.remove('fa-solid')
    document.querySelector(`#i${post_id}`).classList.add('fa-regular')
    document.querySelector(`#s${post_id}`).innerHTML--
  }
  
};
