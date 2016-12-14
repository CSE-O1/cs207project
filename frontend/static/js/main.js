
//plotTS();
function getID(){
    var id = $('#ID').val();
    $.ajax({
        url: '/timeseries/' + id ,
        type: 'GET',
        success: function(response){
            plotTS(response["ts"]);
        },
        error: function(response){
            console.log("Error getting timeseries");
           
        }
    });
   
}


function plotTS(ts){




    $.plot($("#placehold"), [ ts ] );




}

// function printMeta(meta){
//     $("#Meta").html()
//
// }

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

        reader.readAsText(file);
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
    

    console.log(param);
    $.ajax({
        url: '/timeseries',
        type: 'GET',
        data: param,
        success: function(response){
            if(response=="Find nothing!"){
                 $("#Meta").html(response);
            }
            //metaData?
            var retval;
            for (i in response.length){

                for (key in response[i]){
                     retval = retval+ key + ": " + filters[i][key] + "<br>";
                }
            }
            $("#Meta").html(retval);
        },
        error: function(response){
            console.log("Error Finding timeseries");
        }
    });



}


function getID(){
    var id = $('#ID').val();
    $.ajax({
        url: '/timeseries/' + id ,
        type: 'GET',
        success: function(response){
            plotTS(response["ts"]);
        },
        error: function(response){
            console.log("Error getting timeseries");

        }
    });

}


function simGet(){
    var id = $('#simID').val();
    var num= $('#simNum').val();


    $.ajax({
        url: '/simquery/' + id,
        type: 'GET',
        success: function(response){
            plotTS([[response["tst1"], response["tsv1"]], [response["tst2"], response["tsv2"]], [response["tst3"], response["tsv3"] ]]);
        },
        error: function(response){
            console.log("Error Finding timeseries");
        }
    });



}



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















