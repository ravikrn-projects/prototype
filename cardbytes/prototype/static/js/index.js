
function create_table(){
    $.ajax({url: "http://localhost:8000/cardbytes/show_offers?", 
            success: function(result){
                var table_body = "";
                offers = result['offers'];
                for(i=0; i < offers.length; i++){
                    table_body += "<tr>"+
                                      "<td>"+offers[i]['merchant']     +"</td>"+
                                      "<td>"+offers[i]['cashback']*100 +"</td>"+
                                      "<td>"+offers[i]['goal']         +"</td>"+
                                      "<td>"+offers[i]['customer_tag'] +"</td>"+
                                      "<td>"+offers[i]['income_tag']    +"</td>"+
                                  "</tr>";
                }
                var html_code = "<table class='centered responsive-table highlight'>"+
                                    "<thead>" +
                                        "<tr>"+
                                            "<th data-field='merchant'>Merchant</th>"+
                                            "<th data-field='cashback'>Cashback (%)</th>"+
                                            "<th data-field='goal'>Goal</th>"+
                                            "<th data-field='customer_tag'>Customer Tag</th>"+
                                            "<th data-field='income_tag'>Income Tag</th>"+
                                        "</tr>"+
                                    "</thead>"+
                                    "<tbody>"+
                                        table_body+
                                    "</tbody>"+
                                "</table>";
                $('#table').html(html_code);
            }
    });
}

function get_bank_revenue(){
        $.ajax({url: "http://localhost:8000/cardbytes/get_bank_revenue?", 
                success: function(result){
                    var revenue = result['revenue_without_clm'];
                    var revenue_clm = result['revenue_with_clm'];
                    var div = document.getElementById('bank_wo_clm');
                    var div_clm = document.getElementById('bank_clm');
                    div.innerHTML += "<p class='white-text'>"+ revenue + "</p>" 
                    div_clm.innerHTML += "<p class='white-text'>"+ revenue_clm + "</p>" 
                }
        });
}


function get_vendor_revenue(){
        $.ajax({url: "http://localhost:8000/cardbytes/get_vendor_revenue?", 
                success: function(result){
                    var revenue = result['revenue'];
                    var div = document.getElementById('card_revenue');
                    div.innerHTML += "<p class='white-text'>"+ Math.floor(revenue) + "</p>" 
                }
        });
}

function initialize(){
	get_bank_revenue();
	get_vendor_revenue();
    create_table();
}

$(document).ready(initialize);
