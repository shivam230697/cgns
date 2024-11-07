
/*
$(document).ready(function(){
    $('#btn').text('total net weight');
    $( "#btn" ).click(function() {
         var sum = 0;
         $('#newt tbody tr').each(function () {
            var value = parseFloat($(this).find('#' + 'prst').text()) || 0;
            sum += value;
         });
        $('#btn').text('Value: ' + sum);
    });
});
*/


// auto_capitalize.js
$(document).ready(function() {

    $('#id_vehicle_no').on('input', function() {
        var inputValue = $(this).val();
        $(this).val(inputValue.toUpperCase());
    });
});
