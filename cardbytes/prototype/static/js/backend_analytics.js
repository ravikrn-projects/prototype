$(document).ready(function(){
    $.ajax(
            {
                url: get_relevance_data_url, 
                success: function(result){
                   var data = result['data']['index']
                    console.log(data);
                    data.sort();
                 $('#chart-container').highcharts({
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
