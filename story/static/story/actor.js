start_dialog = {
    bubble : "Hi!",
    translation: "",
    options : [],
}
var id_to_dialog = {
    "start": start_dialog,
};

var knowledge_items = []

var storage_id = null;

var image = null;

localStorage.setItem("name","no name");

function restore_actor_data_from_id(id){
    id_to_dialog_text = localStorage.getItem(id)
    if (id_to_dialog_text === null) {
        return null;
    }
    current_id_to_dialog = JSON.parse(id_to_dialog_text)
    if (current_id_to_dialog){
        id_to_dialog = current_id_to_dialog;
    }
    k_items = localStorage.getItem(`${id}_k_items`)
    if(k_items !== null){
        knowledge_items = JSON.parse(k_items)
    }
}

function save_actor_data(){
    localStorage.setItem(storage_id,JSON.stringify(id_to_dialog));
    localStorage.setItem(`${storage_id}_k_items`, JSON.stringify(knowledge_items));
}

function delete_actor_data(){
    localStorage.removeItem(storage_id);
    localStorage.removeItem(`${storage_id}_k_items`);
}

var current_dialog = "start";

function setCurrentDialog() {
    bubble_content = id_to_dialog[current_dialog].bubble;
    document.getElementById('bubble').value = bubble_content;
    translation = id_to_dialog[current_dialog].translation;
    if(translation){
        document.getElementById('translation').value = translation;
    }
    save_actor_data();
}

function setSelection() {
    selection = document.getElementById('selection');
    selection.innerHTML="";
    sel = document.createElement("option");
    sel.innerHTML = "choose target";
    selection.append(sel)
    for( var key in id_to_dialog){
        if (key === current_dialog) {
            continue;
        }
        sel = document.createElement("option");
        sel.innerHTML = key;
        selection.append(sel);
    }
}

function generateTextarea(content) {
    const area = document.createElement("textarea");
    area.innerHTML = content;
    area.rows = "3";
    area.style.borderRadius = "5px";
    area.style.width = "99%";
    return area;
}

function createOptionDropDown(chosen, excluded){
    selection = document.createElement("select");
    opt = document.createElement("option")
    opt.innerHTML = chosen
    selection.append(opt)
    items = ["None"].concat(knowledge_items);
    for (const item of items){
                if(item === chosen){
                    continue;
                }
                if( excluded.includes(item) ){
                    continue;
                }
                opt = document.createElement("option");
                opt.text = item
                selection.append(opt)
    }
    return selection
}

function createButtonDiv(title){
    div = document.createElement("div");
    div.classList.add("btn");
    div.classList.add("btn-secondary");
    div.classList.add("btn-sm");
    div.style.marginLeft = "3px";
    div.style.height = "24px";
    div.style.marginTop = "-5px";
    div.style.fontSize = "12px";
    div.style.padding = "0.25rem 0.5rem";
    div.style.lineHeight = "1";
    div.innerHTML = title;
    return div;
}

function setOptions() {
    console.log(current_dialog);
    current_options = id_to_dialog[current_dialog].options;
    options = document.getElementById('options');
    options.innerHTML = `
    <tr>
        <th> option </th>
        <th> translation </th>
        <th> target </th>
        <th> acquires </th>
        <th> requires </th>
        <th> deactivates </th>
        <th> delete </th>
    </tr>`;
    console.log(current_options)
    current_options.forEach( option => {
        var row = options.insertRow(-1);
        var cell = row.insertCell(0);
        area = generateTextarea(option.content);
        area.onkeyup = event => {
            idx = id_to_dialog[current_dialog].options.indexOf(option);
            console.log(idx);
            id_to_dialog[current_dialog].options[idx].content = event.target.value;
            save_actor_data();
            localStorage.setItem("id_to_dialog",JSON.stringify(id_to_dialog));
        }
        cell.append(area);

        var cell = row.insertCell(1);
        area = generateTextarea(option.translation);
        area.placeholder = "enter high quality translation otherwise a medium translation will be generated for you"
        area.onkeyup = event => {
            idx = id_to_dialog[current_dialog].options.indexOf(option);
            console.log(idx);
            id_to_dialog[current_dialog].options[idx].translation = event.target.value;
            console.log(event.target.value);
            save_actor_data();
            localStorage.setItem("id_to_dialog",JSON.stringify(id_to_dialog));
        }
        cell.append(area);

        var cell = row.insertCell(2);
        cell.innerHTML = option.selection;
        var cell = row.insertCell(3);
        select_acq = createOptionDropDown(option.acquires, [])
        select_acq.onchange = (event) => {
            option.acquires = event.target.value;
            save_actor_data();
            console.log(option.acquires)
        }
        cell.append(selection)
        var cell = row.insertCell(4);
        div = document.createElement("div");
        if(option.requires){
            div.innerHTML = option.requires.toString()
        }
        cell.append(div);
        select1 = createOptionDropDown("None", option.requires)
        uuid2 = crypto.randomUUID();
        select1.id = uuid2 + "s";
        cell.append(select1)
        button = createButtonDiv("add");
        button.id = uuid2;
        button.onclick = (event) => {
            sel = document.getElementById(event.target.id + "s");
            value = sel.options[sel.selectedIndex].text;
            option.requires.push(value);
            save_actor_data();
            setOptions();
            console.log(value);
        }
        cell.append(button);
        var cell = row.insertCell(5);
        div = document.createElement("div");
        if(option.deactivates){
            div.innerHTML = option.deactivates.toString()
        }
        cell.append(div);
        select = createOptionDropDown("None", option.deactivates)
        uuid = crypto.randomUUID();
        select.id = uuid + "s";
        cell.append(selection)
        button = createButtonDiv("add");
        button.id = uuid;
        button.onclick = (event) => {
            sel = document.getElementById(event.target.id + "s");
            value = sel.options[sel.selectedIndex].text;
            option.deactivates.push(value);
            save_actor_data();
            setOptions();
            console.log(value);
        }
        cell.append(button);
        var cell = row.insertCell(6);
        img = document.createElement("img");
        img.src = "/media/delete.png";
        img.style.width = "20px";
        img.onclick = event => {
            const index = current_options.indexOf(option);
            id_to_dialog[current_dialog].options.splice(index,1);
            console.log(id_to_dialog[current_dialog])
            localStorage.setItem("id_to_dialog",JSON.stringify(id_to_dialog));
            setOptions();
        }
        cell.append(img);
    });
    save_actor_data();
}

function createDialogIds() {
    dialogs = document.getElementById('dialogs');
    dialogs.innerHTML = "";
    for(var key in id_to_dialog) {
        let dialog = document.createElement("div");
        dialog.style.color = "black";
        dialog.style.borderRadius = "5px";
        dialog.style.paddingLeft = "5px";
        dialog.innerHTML = key;
        dialog.dataset.id = key;
        if(key === current_dialog){
            dialog.style.background = "#f5eec2";
        }

        dialog.onclick = (event) => {
            current_dialog = event.target.dataset.id;
            c_d = document.getElementById("current_dialog");
            c_d.innerHTML = "Current dialog: " + current_dialog;
            createDialogIds();
            setSelection();
            setOptions();
            setCurrentDialog();
        };

        dialogs.append(dialog);
    }
    save_actor_data();
}

function send_dialog() {
    fetch('dialog', {
        method: 'POST',
        body: JSON.stringify({
            id_to_dialog
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
}
function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    var dataURL = canvas.toDataURL("image/png");

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

function setImage() {

         if( !image ){
            return;
         }

        var img = document.createElement("img");
        img.src = URL.createObjectURL(image);
        img.style.width = "50%";
        img.position = "relative";
        img.style.marginLeft= "auto";
        img.style.marginRight= "auto";
        img.style.display= "block";
        portrait = document.getElementById('portrait');
        portrait.innerHTML="";
        portrait.append(img);
        img.onload = function(){
            imgData = getBase64Image(this);
            localStorage.setItem("image",imgData);
        }
}

function setImageFromStore(){
    var dataImage = localStorage.getItem('image');
    console.log(dataImage);
    if(dataImage == 'null') {
          return null;
    }
    var img = document.createElement("img");
    img.src = "data:image/png;base64," + dataImage;
    img.style.width = "50%";
    img.position = "relative";
    img.style.marginLeft= "auto";
    img.style.marginRight= "auto";
    img.style.display= "block";
    portrait = document.getElementById("portrait");
    portrait.innerHTML="";
    portrait.append(img);
}

function setName(){
    name = document.getElementById("char_name").value;
    localStorage.setItem("name",name);
}

function createChar(){
    id = document.getElementById("id_storage").dataset.sceneid;
    let formData = new FormData()
    formData.append('image', image)
    formData.append('name', name)
    formData.append(
        'knowledge_items',
        JSON.stringify(knowledge_items)
    )
    formData.append(
        'id_to_dialog',
        JSON.stringify(id_to_dialog)
    );
    fetch('/create_character/' + id, {
        method: 'POST',
        body: formData
    }).then( data => {
        story_id = document.getElementById('id_story').dataset.storyid
        scene_id = document.getElementById('id_storage').dataset.sceneid
        console.log("to new location");
        delete_actor_data();
        location.href = `/update_story_scene/${story_id}/${scene_id}`
    })
}

function updateChar(){
    id = document.getElementById("id_actor").dataset.actorid;
    let formData = new FormData();
    formData.append('name', name)
    formData.append('image', image)
    formData.append(
        'id_to_dialog',
        JSON.stringify(id_to_dialog)
    );
    formData.append(
        'knowledge_items',
        JSON.stringify(knowledge_items)
    )
    fetch('/update_character/' + id, {
        method: 'POST',
        body: formData
    }).then( data => {
        story_id = document.getElementById('id_story').dataset.storyid;
        scene_id = document.getElementById('id_storage').dataset.sceneid;
        delete_actor_data();
        location.href = `/update_story_scene/${story_id}/${scene_id}`
    })
}

function set_knowledge_items_from_page() {
    k = document.getElementById("knowledge_items")
    items = k.innerHTML.match(/\b(\w+)\b/g)
    if(!items){
        return items
    }
    items.forEach( item => {
        if( !knowledge_items.includes(item) ){
            knowledge_items.push(item);
        }
    });
    return items;
}


function setKnowledge(){
    item_field = document.getElementById("knowledge");
    item_field.innerHTML = knowledge_items.join(" ");
    setOptions();
    save_actor_data()
}


document.addEventListener( "DOMContentLoaded", () => {

    add_k = document.getElementById("add-k")

    add_k.onclick = () => {
        k_text = document.getElementById("k-text");
        console.log(knowledge_items);
        knowledge_items.push(k_text.value);
        setKnowledge();
    }

    actor_id = document.getElementById("id_actor");
    if ( actor_id ) {
        id = actor_id.dataset.actorid;
        fetch('/get_actor_info/' + id, {
            method: 'GET',
        }).then(response => response.json())
        .then(actor_info => {
            id_to_dialog = actor_info;
            console.log("ID TO DIALOG");
            console.log(id_to_dialog);
            storage_id = `${id}_actor`;
            restore_actor_data_from_id(storage_id);
            set_knowledge_items_from_page();
            setName();
            //console.log(id_to_dialog);
            createDialogIds();
            setCurrentDialog();
            setSelection();
            setOptions();
            setKnowledge();

            //setImageFromStore();
        });
    }
    scene_id = document.getElementById("id_storage");
    console.log(scene_id)
    console.log(actor_id)
    if( scene_id ){
        id = scene_id.dataset.sceneid;
        storage_id = `${id}_scene`
        restore_actor_data_from_id(`${id}_scene`)
    }

    createDialogIds();
    setCurrentDialog();
    setSelection();
    setOptions();
    set_knowledge_items_from_page();
    setKnowledge();
    //setImageFromStore();

    bubble = document.getElementById('bubble');
    bubble.onchange = event => {
        id_to_dialog[current_dialog].bubble = event.target.value;
        console.log(id_to_dialog);
        save_actor_data()
    }

    translation = document.getElementById('translation');
    translation.onchange = event => {
        id_to_dialog[current_dialog].translation = event.target.value;
        console.log(id_to_dialog);
        save_actor_data()
    }

    create_option = document.getElementById('create_option')
    create_option.onclick = () => {
        sel = document.getElementById('selection').value;
        option_content = document.getElementById('option_content').value;
        var option = {
            content: option_content,
            translation:null,
            selection: sel,
            acquires: null,
            requires: [],
            deactivates: []
        }
        id_to_dialog[current_dialog].options.push(option);
        setOptions();
        localStorage.setItem("id_to_dialog",JSON.stringify(id_to_dialog));
    };

    new_dialog = document.getElementById('new_dialog');
    new_dialog.onclick = () => {
        content = document.getElementById('dialog_content').value;
        empty_dialog = {
            bubble: "",
            options: [],
        }
        id_to_dialog[content] = empty_dialog;
        createDialogIds();
        setSelection();
        localStorage.setItem("id_to_dialog",JSON.stringify(id_to_dialog));
    }

    show_dialog = document.getElementById('dialog');
    show_dialog.onclick = () => {
        send_dialog();
    }

    create_char = document.getElementById('create_char');
    if(create_char) {
        create_char.onclick = () => {
            createChar();
        }
    }

    update_char = document.getElementById('update_char');
    if(update_char) {
        update_char.onclick = () => {
            updateChar();
        }
    }

    image_input = document.getElementById('avatar');
    image_input.oninput = function (event) {
        image = event.target.files[0];
        setImage()
        console.log(image)
    }
    char_name = document.getElementById('char_name');
    char_name.onchange = () => {
        setName();
        console.log(localStorage.getItem("name"));
    }
});