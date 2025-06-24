const content = document.getElementById("crowdocs_content");
const navbar = document.getElementById("crowdocs_contentnavbar");

let first_target = document.getElementById("n_1");
let opened = null;
let selected = [];
let display = null;
let include = null;
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
    if (temp_content == display) {return}
    if (display != null) {
        display.setAttribute("class", "hidden");
    }
    if (include != null) {
        include.setAttribute("class", "hidden");
    }
    temp_content.setAttribute("class", "page");
    temp_include.setAttribute("class", "");
    display = temp_content;
    include = temp_include;
    display.scrollTop = 0;
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
    // Set display variable
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
    let max_scroll = max(0, display.scrollHeight - content.clientHeight);
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


// Final
if (first_target != null) {first_target.click()}