const createElem = (tag, attrs = {}, children = []) => {
  const elem = document.createElement(tag);
  Object.assign(elem, attrs);
  children.forEach(child => elem.append(child));
  return elem;
};

const sendFormData = async (endpoint, data) => {
  const formData = new FormData();
  for (const [key, value] of Object.entries(data)) {
    formData.append(key, value);
  }
  await fetch(endpoint, { method: "POST", body: formData });
};

const handleInputChange = (selector, endpoint) => {
  const input = document.getElementById(selector);
  input.onchange = (event) => {
    const id = document.getElementById("bg").dataset[`${selector}id`];
    sendFormData(`${endpoint}/${id}`, { [selector]: event.target.value });
  };
};

const setBackground = () => {
  if (!background) return;

  const img = createElem("img", {
    src: URL.createObjectURL(background),
    style: {
      width: "800px",
      height: "600px",
      position: "relative",
      borderRadius: "5px"
    }
  });

  const bg = document.getElementById("bg");
  bg.innerHTML = "";
  bg.append(img);
};

const placeActor = (actor) => {
  Object.assign(actor.style, {
    transform: `scale(${actor.dataset.scale})`,
    top: actor.dataset.top,
    left: actor.dataset.left
  });
};

const createScene = async (name) => {
  const id = document.getElementById("bg").dataset.storyid;
  const response = await sendFormData(`/create_scene/${id}`, { name });
  const data = await response.json();

  const div = createElem("div", {
    classList: ["scene_selection"],
    style: { width: "100%" },
    dataset: { sceneid: data.scene_id }
  });

  const a = createElem("a", {
    href: `/update_story_scene/${id}/${data.scene_id}`,
    textContent: name
  });

  div.append(a);
  document.getElementById("all_scenes").append(div);
};

const registerAddToSelection = (buttonId, selectionId, displayId, collection) => {
  const button = document.getElementById(buttonId);
  button.dataset.sel_id = selectionId;
  button.onclick = () => {
    const select = document.getElementById(selectionId);
    collection.push(select.value);
    displayItems(displayId, collection);
  };
};

const displayItems = (displayId, collection) => {
  const display = document.getElementById(displayId);
  display.textContent = collection ? collection.toString() : "None";
};

const dragElement = (elmnt) => {
  let [pos1, pos2, pos3, pos4] = [0, 0, 0, 0];

  const dragMouseDown = (e) => {
    e.preventDefault();
    [pos3, pos4] = [e.clientX, e.clientY];
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  };

  const elementDrag = (e) => {
    e.preventDefault();
    [pos1, pos2] = [pos3 - e.clientX, pos4 - e.clientY];
    [pos3, pos4] = [e.clientX, e.clientY];
    elmnt.style.top = `${elmnt.offsetTop - pos2}px`;
    elmnt.style.left = `${elmnt.offsetLeft - pos1}px`;
  };

const closeDragElement = (e) => {
    document.onmouseup = null;
    document.onmousemove = null;
    updatePosScale(e.target);
  };

  if (document.getElementById(`${elmnt.id}header`)) {
    document.getElementById(`${elmnt.id}header`).onmousedown = dragMouseDown;
  } else {
    elmnt.onmousedown = dragMouseDown;
  }
};

const updatePosScale = async (actor) => {
  const { top, left, transform } = actor.style;
  const { charid } = actor.dataset;
  const scale = parseFloat(transform.slice(6, -1));
  await sendFormData(`/set_character_pos_scale/${charid}`, { top, left, scale });
};

const zoom = (event) => {
  event.preventDefault();
  const target = event.target;
  let scale = target.getBoundingClientRect().width / target.offsetWidth;
  scale += event.deltaY * -0.0001;
  scale = Math.min(Math.max(0.05, scale), 4);
  target.style.transform = `scale(${scale})`;
  updatePosScale(target);
};

document.addEventListener("DOMContentLoaded", () => {
  const requires = [];
  const deactivates = [];

  registerAddToSelection("add_dea", "deactivates", "display_dea", deactivates);
  registerAddToSelection("add_req", "requires", "display_req", requires);

  document.querySelectorAll(".actor").forEach((actor) => {
    placeActor(actor);
    actor.onwheel = zoom;
    dragElement(actor);
  });

  const rightBox = document.getElementById("right_box");
  rightBox.style.width = `${window.innerWidth - 860}px`;

  handleInputChange("story_name", "/set_story_name");
  handleInputChange("name", "/set_scene_name");
  handleInputChange("description", "/set_scene_description");

  const backgroundInput = document.getElementById("bgi");
  backgroundInput.oninput = (event) => {
    const id = document.getElementById("bg").dataset.sceneid;
    background = event.target.files[0];
    setBackground();
    sendFormData(`/background/${id}`, { image: background });
  };

  const addScene = document.getElementById("add_scene");
  addScene.onclick = () => {
    const name = document.getElementById("scene_name").value;
    document.getElementById("scene_name").value = "";
    createScene(name);
  };

  const deleteScenes = document.getElementsByClassName("del_scene");
  for (const deleteScene of deleteScenes) {
    deleteScene.onclick = (event) => {
      const id = event.target.dataset.sceneid;
      fetch(`/delete_scene/${id}`, { method: "POST" });
    };
  }
});