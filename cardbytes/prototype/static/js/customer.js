
function buy(){
    console.log($("#amount").val());
    $.ajax(
            {
                url: "http://127.0.0.1:8000/cardbytes/transact", 
                data: {
                        user_id: user_id,
                        amount: $("#amount").val(),
                        merchant_id: 48
                },
                success: function(result){
                    console.log(result);
                    updateUserData();
                }
            }
    );
}

function updateUserData(){
    $.ajax(
            {
                url: "http://127.0.0.1:8000/cardbytes/user?user_id="+user_id, 
                success: function(result){
                    $("#textarea1").val(result.user.message);
                    $("#acc_balance").html("Account Balance: "+result.user.acc_balance);
                    $("#cashback").html("Cashback: "+result.user.cashback_realized);
                }
            }
    );
}       

function updateMerchantData(){
    $.ajax(
            {
                url: "http://127.0.0.1:8000/cardbytes/get_merchants", 
                success: function(result){
                    console.log(result);
                    var list_items = "";
                    for(var i=0;i<result.merchants.length;i++)
                        list_items += "<li><a href='#!'>"+ result.merchants[i].name +"</a></li>";
                    $("#dropdown1").html(list_items);
                    $("#merchant").html(result.merchants[0].name);
                }
            }
        );
}

function initialize(){
    updateUserData();
    updateMerchantData();
}

$(document).ready(initialize());
