let delayTimer;

$('#id_results').keyup(function() {
    clearTimeout(delayTimer);
    $('#id_results').text('Looking...');
});