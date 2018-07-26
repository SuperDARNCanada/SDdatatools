$("#plot-type").change(function() {
    var plot = $( '#plot-type option:selected' ).val();
    if(plot=="RTI")
    {
        $("#rti").show();
    }
    else if(plot=="Convection")
    {
        $("#convection").show();
    }
    else
    {
        $("#fan").show();
    }

})
