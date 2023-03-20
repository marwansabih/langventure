background = null;

current_id_to_dialog = null;

current_id = null;

user_knowledge = []


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
    console.log(actor.dataset.scale)
    actor.style.transform = `scale(${actor.dataset.scale})`;
    actor.style.top = actor.dataset.top;
    actor.style.left = actor.dataset.left;
}

function scale_dialog(){
    field = document.getElementById("dialog_field")
    field.style.width = `${window.innerWidth-880}px`
    console.log(`{$window.innerWidth-850}px`)
}

function contains_all_requirements(reqs){
    if( reqs.length === 0 ){
        return true;
    }

    return reqs.every( (req) => {
        return user_knowledge.includes(req);
    })
}

function not_deactivated(deactivations){
    if( deactivations.length === 0 ){
        return true;
    }
    return !deactivations.every( (dea) => {
        return user_knowledge.includes(dea);
    })
}

function set_dialog(){
            start = current_id_to_dialog[current_id];
            bubble = document.getElementById("bubble");
            bubble.innerHTML = start["bubble"];
            bubble.onclick = () => {
                translation = document.getElementById("translation");
                translation.innerHTML = start["translation"];
            }

            options = start["options"];
            opts = document.getElementById("options");
            opts.innerHTML = ""
            options.forEach( option => {
                div = document.createElement("div");
                div.style.padding = "3px";
                description = document.createElement("div");
                description.innerHTML = `${option["content"]}`
                description.style.display = "inline-block";
                description.style.width = "95%";
                description.style.verticalAlign = "middle";
                description.style.padding = "5px";
                description.onclick = () => {
                    translation = document.getElementById("translation");
                    translation.innerHTML = option["translation"];
                }
                label = document.createElement("div")
                label.style.display = "inline-block";
                label.style.borderRadius = "5px";
                label.style.padding = "5px";
                label.className = "btn btn-secondary"
                label.innerHTML = "&#x2192;"
                label.style.width = "5%";
                label.style.verticalAlign = "middle";
                container = document.createElement("div");
                container.style.verticalAlign = "middle";
                container.append(label);
                container.append(description);
                div.append(container);
                label.dataset.next = option["selection"];
                label.dataset.acquires = option["acquires"];
                console.log("acquires");
                console.log(option["acquires"]);
                label.onclick =  e => {
                    current_id = e.target.dataset.next;
                    acquires = e.target.dataset.acquires;
                    if(acquires !== "null" && !user_knowledge.includes(acquires) ){
                        user_knowledge.push(acquires);
                        update_user_knowledge(acquires);
                    }
                    console.log(current_id);
                    set_dialog();
                };
                console.log("requires")
                console.log(option["requires"])
                if(contains_all_requirements(option["requires"])
                   && not_deactivated(option["deactivates"]) ){
                    opts.append(div);
                }
            });
}


function add_dialog(actor){
    actor.onclick = (e) => {
        target = e.target;
        hide = document.getElementById("hide")
        hide.style.display = "block";
        id = target.dataset.charid;
        fetch(`/get_dialog/${id}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(dialog_info => {
            current_id_to_dialog = dialog_info["id_to_dialog"];
            current_id = "start";
            n = dialog_info["name"];
            name_header = document.getElementById("name");
            name_header.innerHTML = `${n} says:`;
            set_dialog();
        });

    }
}

function update_user_knowledge(item){
    let story_id = document.getElementById("story_id").dataset.storyid;
    let scene_id = document.getElementById("scene_id").dataset.sceneid;
    let formData = new FormData();
    formData.append('item', item);
    formData.append('story_id', story_id);
    fetch('/update_user_knowledge', {
        method: 'POST',
        body: formData
    }).then(
        set_active_scenes()
    )

}

function set_existing_user_knowledge(){
    const items = document.getElementsByClassName("knowledge_item")
    Array.from(items).forEach( item => {
        k_i = item.dataset.item;
        user_knowledge.push(k_i);
    })
    set_active_scenes()
}

function set_active_scenes(){
    const scene_id = document.getElementById("scene_id").dataset.sceneid;
    const story_id = document.getElementById("story_id").dataset.storyid;
    fetch('/get_active_scenes/' + scene_id, {
        method: 'GET'
    }).then( response => response.json()
    ).then( data => {
        active_scenes = data["scenes"]
        ids = data["ids"]
        current_id = data["current_id"]
        scene_div = document.getElementById("scenes")
        scene_div.innerHTML = "";
        active_scenes.forEach( (scene, idx) => {
            a = document.createElement("a")
            a.href = `/story_scene/${story_id}/${ids[idx]}`
            a.classList.add("btn")
            if(ids[idx] === current_id){
                a.classList.add("btn-primary")
            }else{
                a.classList.add("btn-secondary")
            }
            a.style.marginLeft="3px"
            a.innerHTML = scene
            scene_div.append(a)
            console.log(a)
        });
    })
}

document.addEventListener( "DOMContentLoaded", () => {
    scale_dialog();
    window.onresize = () => {
        scale_dialog();
    };
    set_active_scenes();
    set_existing_user_knowledge();
    document.querySelectorAll(".actor").forEach( actor => {
        place_actor(actor);
        add_dialog(actor);
    })
    background_input = document.getElementById("bgi");
});