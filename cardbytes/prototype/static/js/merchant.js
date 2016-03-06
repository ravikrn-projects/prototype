var tags = [
             {name: "High Paying", id: 0},
             {name: "Low Paying", id: 1}, 
             {name: "Coffee Lovers", id: 2}
];

var geography = [
             {name: "Delhi", id: 0},
             {name: "Mumbai", id: 1} 
];

var goals = [
             {name: "Loyalty program", id: 0},
             {name: "New customer acquisition", id: 1}, 
             {name: "Blast marketing", id: 2}
];

function updateDropDownList(id, item, type){
    $("#"+type).html(item);
    eval("selected_"+type+"="+id);
}

function loadDropDownList(items, type){
    var list_items = "";
    for(var i=0;i<items.length;i++){
        var item = items[i];
        var onclick = "onClick=\"updateDropDownList(" +  item.id + ", "+ "'"+ item.name + "'"+","+ "'"+type +"'"+ ")\"";
        list_items += "<li><a href='#!' "+onclick+">"+ item.name +"</a></li>";
    }
    $("#"+type+"_dropdown").html(list_items);
    $("#"+type).html(items[0].name);
    eval("selected_"+type+"=0");
}

function initialize(){
    loadDropDownList(goals, "goal");
    loadDropDownList(tags, "tag");
    loadDropDownList(geography, "geography");
}

$(document).ready(initialize);
