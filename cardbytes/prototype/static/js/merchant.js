
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
                    url: generate_offer_url,
                    data: {
                            merchant_id: merchant_id,
                            cashback: $("#cashback").val(),
                            goal_id: selected_goal,
                            // income_tag_id: selected_income_tag,
                            // customer_tag_id: selected_customer_tag,
                    },
                    success: function(result){
                        if(result.success == true)
                            $('#generate_msg').html("<span class='success'>Offer successfully generated.</span>");
                        else
                            $('#generate_msg').html("<span class='failure'>An error occured.</span>");
                    }
                }
        );
}

function loadChart(){
    $.ajax({url: get_transaction_data_url,
            data: {
                    merchant_id: merchant_id,
            },
            success: function(result){
                var data = result['data']
                $('#chart_container').highcharts({
                    chart: {
                        type: 'line'
                    },
                    title: {
                        text: 'Transaction Data'
                    },
                    xAxis: {
                        categories: data.x
                    },
                    yAxis: [
                        {
                            title: {
                                text: 'Sales'
                            }
                        },
                        {
                            title: {
                                text: 'Cashback'
                            },
                            opposite: true
                        }
                    ],
                    series: [
                        {
                            name: data.y[0].name,
                            data: data.y[0].data,
                            yAxis: 0
                        },
                        {
                            name: data.y[1].name,
                            data: data.y[1].data,
                            yAxis: 1
                        }
                    ]
                });
            }
        }
    );
}

function initialize(){
    loadDropDownList(goals, "goal");
    // loadDropDownList(income_tag, "income_tag");
    // loadDropDownList(customer_tag, "customer_tag");
    loadChart();
}

$(document).ready(initialize);
