$(document).ready(function(){
    $.ajax(
            {
                url: "http://localhost:8000/cardbytes/get_relevance_data?", 
                success: function(result){
                   var data = result['data']['index']
                    console.log(data);
                    data.sort();
                 $('#container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'Relevance data'
        },
        xAxis: {
            categories: ['Users']
        },
        yAxis: {
            title: {
                text: 'Relevance index'
            }
        },
        series: [{
            data: data
        }]
            });
        
                }
            }
    );

})