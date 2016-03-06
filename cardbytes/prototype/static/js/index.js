
function generate_offers(){ 
	$('#generate_offers').on('click',  function(){
        $.ajax(
        		{	
        			url: "http://localhost:8000/cardbytes/generate_offers?", 
          			success: function(result){
        				console.log('success');
        			}
        		}
        	);
      }
    );
}

function create_table(){
		$('#generate_offers').on('click',  function(){
        $.ajax(
        		{	
        			url: "http://localhost:8000/cardbytes/generate_offers?", 
          			success: function(result){
        				console.log('success');
        			}
        		}
        	);
      	}
    );

        $.ajax({url: "http://localhost:8000/cardbytes/show_offers?", 
        	success: function(result){
        	console.log(result);
 		var div = document.getElementById('table');
       var html_code = "<table class='centered responsive-table highlight'>" +
       "<thead>" +
          "<tr>"+
             "<th data-field='id'>User</th>"+
             "<th data-field='merchant'>Merchant</th>"+
             "<th data-field='cashback'>Cashback (%)</th>"+
             "<th data-field='cashback_used'>Cashback Used</th>"+
          "</tr>"+
        "</thead>"+
        "<tbody>";
        offers = result['offers'];
        for(i=0; i < offers.length; i++){
       html_code += "<tr>";
       	
        	html_code += "<td>"+offers[i]['user_id']+"</td>";
        	html_code += "<td>"+offers[i]['merchant']+"</td>";
        	html_code += "<td>"+offers[i]['cashback']*100+"</td>";
        	html_code += "<td>"+offers[i]['cashback_used']+"</td>";
        	html_code += "</tr>";
        	
        }
        html_code += "</tbody>"+ "</table>";
        div.innerHTML = html_code;
    }});
}

function get_bank_revenue(){
	 $(document).ready(function(){
        $.ajax({url: "http://localhost:8000/cardbytes/get_bank_revenue?", 
          success: function(result){
          var revenue = result['revenue_without_clm'];
          var revenue_clm = result['revenue_with_clm'];
          var div = document.getElementById('bank_wo_clm');
          var div_clm = document.getElementById('bank_clm');
          div.innerHTML += "<p class='white-text'>"+ revenue + "</p>" 
          div_clm.innerHTML += "<p class='white-text'>"+ revenue_clm + "</p>" 
        }});
      });
}


function get_vendor_revenue(){
	$(document).ready(function(){
        $.ajax({url: "http://localhost:8000/cardbytes/get_vendor_revenue?", 
          success: function(result){
          var revenue = result['revenue'];
          var div = document.getElementById('card_revenue');
          div.innerHTML += "<p class='white-text'>"+ Math.floor(revenue) + "</p>" 
        }});
      });
}

function initialize(){
	get_bank_revenue();
	get_vendor_revenue();

}

$(document).ready(initialize());