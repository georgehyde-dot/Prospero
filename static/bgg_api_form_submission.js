$("#apiSearchForm").submit(function(e) {
    e.preventDefault();

    let formData = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'method': $('#id_method option:selected').text() // Assuming this is how you get the method name
    };

    // Collect dynamic filter values
    $("#modifierInput input").each(function() {
        if($(this).attr('type') === 'checkbox') {
            formData[$(this).attr('name')] = $(this).is(':checked');
        } else if($(this).val().trim() !== '') {
            formData[$(this).attr('name')] = $(this).val().trim();
        }
    });

    $.ajax({
        url: 'data', 
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(formData),
        success: function(response) {
            // Handle the response from the server
        },
        error: function(error) {
            // Handle error
        }
    });
});
