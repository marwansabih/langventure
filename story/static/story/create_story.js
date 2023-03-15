background = null;

function update_pos_scale(actor){
    z = actor.style.top;
    left = actor.style.left;
    scale = actor.style.transform;
    id = actor.dataset.charid;
    let formData = new FormData();
    formData.append('top', z);
    formData.append('left', left);
    formData.append('scale', scale.substring(6, scale.length-1));
    fetch('/set_character_pos_scale/' + id, {
       method: 'POST',
       body: formData
    })
}

function zoom(event) {
    target = event.target
    let scale = target.getBoundingClientRect().width / target.offsetWidth;
    event.preventDefault();
    scale += event.deltaY * -0.0001;

    // Restrict scale
    scale = Math.min(Math.max(.05, scale), 4);
    console.log(scale);

    // Apply scale transform
    event.target.style.transform = `scale(${scale})`;
    update_pos_scale(event.target);
}

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById(elmnt.id + "header")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement(e) {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
        update_pos_scale(e.target);
    }
}

function setBackground() {

         if( !background ){
            return;
         }

        var img = document.createElement("img");
        img.src = URL.createObjectURL(background);
        img.style.width = "800px";
        img.style.height = "600px";
        img.position = "relative";
        img.style.borderRadius = "5px";
        bg = document.getElementById('bg');
        bg.innerHTML="";
        bg.append(img);
        img.onload = function(){
            /*imgData = getBase64Image(this);
            localStorage.setItem("bg",imgData);*/
        }
}

function place_actor(actor) {
    console.log(actor.dataset)
    console.log(actor.dataset.top)
    actor.style.transform = `scale(${actor.dataset.scale})` //actor.dataset.scale;
    console.log(actor.dataset.scale);
    actor.style.top = actor.dataset.top;
    actor.style.left = actor.dataset.left;
}

function create_scene(name) {
    id = document.getElementById("bg").dataset.storyid;
    formData = new FormData();
    formData.append('name', name);
    fetch('/create_scene/' + id, {
        method: 'POST',
        body: formData
    }).then(
        response => response.json()
    ).then (
        data => {
            div = document.createElement("div");
            div.classList.add("scene_selection");
            div.style.width = "100%";
            div.dataset.sceneid = data.scene_id;
            a = document.createElement("a");
            a.href = `/update_story_scene/${id}/${data.scene_id}`;
            a.innerHTML = name;
            div.append(a);
            all_scenes = document.getElementById("all_scenes");
            all_scenes.append(div);
        }
    )
}

function enable_scene_selection() {
    const scene_selections = document.getElementsByClassName("scene_selection")
    scene_selections.forEach( selection => {
        selection.onclick = event => {

        }
    });
}

function register_add_to_selection(button_id, selection_id, display_id, collection) {
    button = document.getElementById(button_id);
    button.dataset.sel_id = selection_id
    button.onclick = (element) => {
        select = document.getElementById(selection_id)
        collection.push(select.value)
        display_items(display_id, collection)
    }
}

function display_items(display_id, collection) {
    display = document.getElementById(display_id)
    display.innerHTML = "None"
    if (collection){
        display.innerHTML = collection.toString();
    }
}

document.addEventListener( "DOMContentLoaded", () => {

    requires = []
    deactivates = []
    console.log("here here here")

    register_add_to_selection("add_dea", "deactivates", "display_dea", deactivates)
    register_add_to_selection("add_req", "requires", "display_req", requires)

    document.querySelectorAll(".actor").forEach( actor => {
        place_actor(actor);
        actor.onwheel = zoom;
        dragElement(actor);
    })

    console.log("after?")

    right_box = document.getElementById("right_box");
    console.log(`${window.innerHeight - 820}px`);
    right_box.style.width = `${window.innerWidth - 860}px`;

    //handle story name
    na = document.getElementById("story_name");
    na.onchange = event => {
        id = document.getElementById("bg").dataset.storyid;
        console.log(id);
        let formData = new FormData();
        formData.append('name', event.target.value);
        fetch('/set_story_name/' + id, {
            method: 'POST',
            body: formData
        });
    }

    //handle scene name
    na = document.getElementById("name");
    na.onchange = event => {
        id = document.getElementById("bg").dataset.sceneid;
        let formData = new FormData();
        formData.append('name', event.target.value);
        fetch('/set_scene_name/' + id, {
            method: 'POST',
            body: formData
        });
    }

    //handle description
    desc = document.getElementById("description");
    desc.onchange = event => {
        id = document.getElementById("bg").dataset.sceneid;
        let formData = new FormData();
        formData.append('description', event.target.value);
        fetch('/set_scene_description/' +id, {
            method: 'POST',
            body: formData
        });
    }

    //handle background
    background_input = document.getElementById("bgi");
    background_input.oninput = function (event) {
        id = document.getElementById("bg").dataset.sceneid;
        background = event.target.files[0];
        setBackground();
        let formData = new FormData()
        formData.append('image', background)
        fetch('/background/' + id, {
            method: 'POST',
            body: formData
        })
    }

    //handle adding new scene
    add_scene = document.getElementById("add_scene")
    add_scene.onclick = () => {
        name = document.getElementById("scene_name").value;
        document.getElementById("scene_name").value = "";
        console.log(name);
        create_scene(name);
    }

    delete_scenes = document.getElementsByClassName("del_scene");
    for( delete_scene in delete_scenes){
        delete_scenes[delete_scene].onclick = event => {
            id = event.target.dataset.sceneid;
            console.log("I");
            fetch('/delete_scene/' +id, {
            method: 'POST'
            })
        }
    };
});