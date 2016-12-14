
//plotTS();
function getID(){
    var id = $('#ID').val();
    var response_from_server;
    $.ajax({
        url: '/timeseries/' + id ,
        type: 'GET',
        success: function(response){
            console.log("success");
            response_from_server=response;
            console.log(response);
        },
        error: function(response){
            console.log("error");
            console.log(response);
            console.log("Error getting timeseries from sm");
        }
    });
    // console.log(response_from_server);

    plotTS(response_from_server);

}

function plotTS(ts){
    var series=[1,2,3,4,5];
    $.plot($("#placeholder"), [ [[0, 0], [1, 1]] ], { yaxis: { max: 1 }});

}

