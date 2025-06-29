const content = document.getElementById("crowdocs_content");
const navbar = document.getElementById("crowdocs_navbar");
const nav_content = document.getElementById("nav_content");
const include_bar = document.getElementById("crowdocs_include_bar");

let first_target = document.getElementById("n_1");
let opened = null;
let selected = [];
let display = {
    "content":null,
    "navbar":nav_content,
    "include_bar":null,
};
let simclick = false;

function min(a, b) {
    if (a<=b) {return a}
    return b;
}
function max(a, b) {
    if (a>=b) {return a}
    return b;
}

function show_content(id) {
    let number = id.split("_").pop();
    let temp_content = document.getElementById("c_" + number);
    let temp_include = document.getElementById("ic_" + number);
    if (temp_content == display["content"]) {return}
    if (display["content"] != null) {
        display["content"].setAttribute("class", "hidden");
    }
    if (display["include"] != null) {
        display["include"].setAttribute("class", "hidden");
    }
    temp_content.setAttribute("class", "page");
    temp_include.setAttribute("class", "");
    display["content"] = temp_content;
    display["include"] = temp_include;
    content.scrollTop = 0;
}

function deselect_all() {
    let new_selected = [];
    for (let x=0; x<selected.length; x++) {
        let item = selected[x];
        if (item == opened) {new_selected.push(item); continue}
        item.setAttribute("class", "not_selected");
    }
    selected = new_selected;
}

function show_sub(item) {
    if (simclick) {return}
    console.log("show sub " + item.target);
    let target = item.target;
    show_content(target.id);
    deselect_all();
    target.setAttribute("class", "selected");
    selected.push(target);
}

function show(item) {
    if (simclick) {return}
    console.log("show " + item.target);
    let target = item.target;

    show_content(target.id);

    target.setAttribute("class", "selected");
    selected.push(target);
    simclick = true;
    // Set display["content"] variable
    if (opened != null) {
        // setTimeout(opened.click, 100)
        opened.click();
    }
    simclick = false;
    opened = target;
    deselect_all();
}

function getElementYOffset(elem) {
    let offsetTop = 0;
    while (elem) {
        offsetTop += elem.offsetTop;
        elem = elem.offsetParent;
    }
    return offsetTop;
}

function view(item) {
    let screenPosition = getElementYOffset(item);
    let max_scroll = max(0, display["content"].scrollHeight - content.clientHeight + 20);
    content.scrollTop = min(max_scroll, screenPosition);
}

function do_include(item) {
    if (simclick) {return}
    let target = item.target;
    console.log(target);
    if (target.tagName.toLowerCase() == "summary") {
        simclick = true;
        target.click();
        simclick = false;
    }
    // console.log(target)
    let id = target.id.split("_").pop();
    let elem = document.getElementById("h_" + id);
    view(elem);
}

function toggle_dropdown(item) {
    let target = item.target;
    console.log(target);
    let id = target.id.split("_").pop();
    let elem = document.getElementById("d_" + id);
    if (elem.getAttribute("class") == "dropdown") {
        console.log("Close");
        elem.setAttribute("class", "dropdown hidden");
        target.setAttribute("class", "dropdown_close");
    } else {
        console.log("Open");
        elem.setAttribute("class", "dropdown");
        target.setAttribute("class", "dropdown_open");
    }
}

// scroll handler
function handle_scroll(target){
    function hndlr(event){
        let screenPosition = this.scrollTop + (event.deltaY/10);
        let max_scroll = max(0, display[target].scrollHeight - this.clientHeight + 20);
        this.scrollTop = max(0, min(max_scroll, screenPosition));
    }
    return hndlr
}

content.addEventListener("wheel", handle_scroll("content"));
include_bar.addEventListener("wheel", handle_scroll("include"));
navbar.addEventListener("wheel", handle_scroll("navbar"));

// Navigation initialization
for (let x=1; x<999; x++) {
    let elem = document.getElementById("n_" + x);
    if (elem == null) {break}
    if (elem.tagName.toLowerCase() == "summary") {
        elem.addEventListener("click", show);
    } else {
        elem.addEventListener("click", show_sub);
    }
}

for (let x=1; x<999; x++) {
    let elem = document.getElementById("i_" + x);
    if (elem == null) {break}
    if (elem.tagName.toLowerCase() == "summary"){
        elem.click();
    }
    elem.addEventListener("click", do_include);
}

// Dropdown initialization
for (let x=1; x<999; x++) {
    let elem = document.getElementById("db_" + x);
    if (elem == null) {break}
    elem.addEventListener("click", toggle_dropdown)
}

// Final
if (first_target != null) {first_target.click()}