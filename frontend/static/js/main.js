
//plotTS();
function getID(){
    var id = $('#ID').val();
    var response_from_server;
    $.ajax({
        url: '/timeseries/' + id ,
        type: 'GET',
        success: function(response){
            response_from_server=response;
        },
        error: function(response){
            console.log("Error getting timeseries");
        }
    });
    console.log(response_from_server);

    plotTS(response_from_server["tsdata"]);

}

function plotTS(ts){

    var fake_MataData = {"id": 1, "mean":24, "std": 0.3, "blarg":0.5, "level":"A" };
    var fake_timeSeries = ([4,5,6],[1,2,3]);
    console.log(ts);
    $.plot($("#placeholder"), [ ts[1], ts[0] ], { yaxis: { max: 1 }});


}

function printMeta(meta){


}

function storeTS(){
    var file = $("#tsFile")[0];
    console.log(file);
    var f = file.files[0];
    // var $.getJSON("test.json", function(json) {
    //     console.log(json);
    // });


    console.log(f);

    var reader = new FileReader();
    reader.onload = function(e){

        var ts_JASON = e.target.result;
        console.log(ts_JASON);

        $.ajax({
            url: '/timeseries',
            type: 'POST',
            data: ts_JASON,
            success: function(response){
                console.log(response);
              plotTS(response);
            },
            error: function(error){
                console.log(response);
              console.log("Error storing timeseries");
            }
          });
    };

    

}

function filter(){
    var level = $('#level_in').val();
    var mean = $('#mean_in').val();
    var param;
    if(level==""){
        param = {"mean_in" : mean};
    }else{
        param = {"level_in" : level};
    }
   

    $.ajax({
        url: '/timeseries',
        type: 'GET',
        data: param,
        success: function(response){
            //metaData?
            plotTS(response);
        },
        error: function(response){
            console.log("Error Finding timeseries");
        }
    });



}


function simGet(){
    var id = $('#simID').val();
    var num= $('#simNum').val();


        $.ajax({
        url: '/simquery',
        type: 'GET',
        data: {"id": id, "n": num},
        success: function(response){
            plotTS(response);
        },
        error: function(response){
            console.log("Error Finding timeseries");
        }
    });



}

function simGetShow(){}

function simPost(){
        var file = $("#simPostFile")[0];
        console.log(file);
        var f = file.files[0];

            $.ajax({
            url: '/simquery',
            type: 'POST',
            data: ts_JASON,
            success: function(response){
                console.log(response);
              plotTS(response);
            },
            error: function(error){
                console.log(response);
              console.log("Error storing timeseries");
            }
          });
    };

}















