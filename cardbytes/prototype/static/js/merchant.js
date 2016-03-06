
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

function generateOffer(){
    if($('#cashback').val() === "")
        $('#generate_msg').html("<span class='failure'>Enter cashback value.</span>");
    else
        $.ajax(
                {
                    url: "http://127.0.0.1:8000/cardbytes/generate_offer", 
                    data: {
                            merchant_id: merchant_id,
                            cashback: $("#cashback").val(),
                            goal_id: selected_goal,
                            customer_tag_id: selected_tag,
                            geography_id: selected_geography,
                    },
                    success: function(result){
                        $('#generate_msg').html("<span class='success'>Offer successfully generated.</span>");
                    }
                }
        );
}

function initialize(){
    loadDropDownList(goals, "goal");
    loadDropDownList(tags, "tag");
    loadDropDownList(geography, "geography");
}

$(document).ready(initialize);
