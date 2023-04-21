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
    actor.style.transform = `scale(${actor.dataset.scale})`;
    actor.style.top = actor.dataset.top;
    actor.style.left = actor.dataset.left;
}

function scale_dialog(){
    field = document.getElementById("dialog_field")
    field.style.width = `${window.innerWidth-880}px`
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


function createAudioElement(audioSrc) {
    var audioElement = document.createElement("audio");
    audioElement.src = audioSrc;

    var playButton = document.createElement("button");
    playButton.textContent = "Play";

    playButton.addEventListener("click", function () {
        if (audioElement.paused) {
            audioElement.play();
            playButton.textContent = "Pause";
        } else {
            audioElement.pause();
            playButton.textContent = "Play";
        }
    });

    var progressBar = document.createElement("input");
    progressBar.type = "range";
    progressBar.min = 0;
    progressBar.value = 0;
    progressBar.step = 1;

    var currentTimeDisplay = document.createElement("span");

    audioElement.addEventListener("loadedmetadata", function () {
        progressBar.max = Math.floor(audioElement.duration);
        currentTimeDisplay.textContent = formatTime(audioElement.currentTime);
    });

    audioElement.addEventListener("timeupdate", function () {
        progressBar.value = Math.floor(audioElement.currentTime);
        currentTimeDisplay.textContent = formatTime(audioElement.currentTime);
    });

    progressBar.addEventListener("input", function () {
        audioElement.currentTime = progressBar.value;
    });

    function formatTime(seconds) {
        var minutes = Math.floor(seconds / 60);
        var remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
    }

    var audioContainer = document.createElement("div");
    audioContainer.className = "audio-container";
    audioContainer.appendChild(playButton);
    audioContainer.appendChild(progressBar);
    audioContainer.appendChild(currentTimeDisplay);
    audioContainer.appendChild(audioElement);

    return audioContainer;
}

function set_dialog(){
            translation.innerHTML = "No text selected"
            translation.style.height = "auto"
            bubble = document.getElementById("bubble");
            start = current_id_to_dialog[current_id];
            bubble.innerHTML = start["bubble"];
            bubble.onclick = () => {
                translation = document.getElementById("translation");
                translation.style.whiteSpace= "pre-wrap";
                translation.style.overflowY = "scroll";
                const translationRect = translation.getBoundingClientRect();
                const windowHeight = window.innerHeight;
                const dynamicHeight = windowHeight - translationRect.top - 50;
                translation.style.height = `${dynamicHeight}px`;
                translation.innerHTML = start["bubble"] + "\n\n" + start["translation"];
            }

            if (start.audio) {
                container = createAudioElement(start.audio)
                bubble.appendChild(container)
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
                    translation.style.whiteSpace= "pre-wrap";
                    translation.style.overflowY = "scroll";
                    const translationRect = translation.getBoundingClientRect();
                    const windowHeight = window.innerHeight;
                    const dynamicHeight = windowHeight - translationRect.top - 50;
                    translation.style.height = `${dynamicHeight}px`;
                    translation.innerHTML = option["content"] + "\n\n" + option["translation"];
                }
                label = document.createElement("div");
                label.className = "custom-label";
                label.innerHTML =  "&#x2192;";
                container = document.createElement("div");
                container.style.verticalAlign = "middle";
                container.append(label);
                container.append(description);
                div.append(container);
                label.dataset.next = option["selection"];
                label.dataset.acquires = option["acquires"];
                label.onclick =  e => {
                    translation = document.getElementById("translation")
                    acquires = e.target.dataset.acquires;
                    console.log("acquires")
                    console.log(acquires)
                    if(acquires !== "null" && !user_knowledge.includes(acquires) ){
                        user_knowledge.push(acquires);
                        update_user_knowledge(acquires);
                    }
                    if (current_id === e.target.dataset.next)
                    {
                        set_active_scenes()
                        hide = document.getElementById("hide");
                        hide.style.display = "None"
                        return ""
                    }
                    current_id = e.target.dataset.next;
                    console.log(current_id);
                    set_dialog();
                };
                if(contains_all_requirements(option["requires"])
                   && not_deactivated(option["deactivates"]) ){
                    opts.append(div);
                }
                if (option.audio) {
                    var audioContainer = createAudioElement(option.audio);
                    div.appendChild(audioContainer)
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

async function update_user_knowledge(item){
    let story_id = document.getElementById("story_id").dataset.storyid;
    let scene_id = document.getElementById("scene_id").dataset.sceneid;
    let formData = new FormData();
    console.log(item)
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
            //const scene_id = document.getElementById("scene_id").dataset.sceneid;
            //const story_id = document.getElementById("story_id").dataset.storyid
        })
    })
}

function acquire_collectible(collectible) {
  collectible.onclick = async event => {
    item = event.target.dataset.knowledge_item;
    name = event.target.dataset.name;
    await update_user_knowledge(item);
    await showDialog(name);
    const scene_id = document.getElementById("scene_id").dataset.sceneid;
    const story_id = document.getElementById("story_id").dataset.storyid;
    location.href = "/story_scene/" + story_id + "/" + scene_id;
  }
}

async function showDialog(item) {
  const item_acquired = document.getElementById('item_acquired');
  const acquired_item = item_acquired.querySelector('.acquired-item');
  acquired_item.textContent = `${item}`;
  item_acquired.style.display = 'block';

  return new Promise(resolve => setTimeout(() => {
    item_acquired.style.display = 'none';
    resolve();
  }, 3000));
}

document.addEventListener( "DOMContentLoaded", () => {
    document.documentElement.style.overflow = "hidden"
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
    document.querySelectorAll(".collectible").forEach( collectible => {
        place_actor(collectible);
        acquire_collectible(collectible);
    })
    background_input = document.getElementById("bgi");
});