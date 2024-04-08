$(document).ready(function() {
    $('#id_method').change(function() {
        var methodId = $(this).val();
        console.log("Method selected: ", methodId);  // Log selected method ID

        if (methodId) {
            $.ajax({
                url: '/data/get_modifiers/' + methodId,
                type: 'GET',
                success: function(modifiers) {
                    console.log("Modifiers received: ", modifiers);  // Log received data
                    var modifierHtml = '';
                    modifiers.forEach(function(modifier) {
                        if (modifier.modifier_type === 'bool') {
                            modifierHtml += '<div><label>' + modifier.modifier_name + 
                                            ': <input type="checkbox" name="' + modifier.modifier_name + 
                                            '" value="true"></label></div>';
                        } else if (modifier.modifier_type === 'text') {
                            modifierHtml += '<div><label>' + modifier.modifier_name + 
                                            ': <input type="text" name="' + modifier.modifier_name + 
                                            '"></label></div>';
                        } else if (modifier.modifier_type === 'int') {
                            modifierHtml += '<div><label>' + modifier.modifier_name + 
                                            ': <input type="text" name="' + modifier.modifier_name + 
                                            '"></label></div>';
                        }
                    });
                    $('#modifierInput').html(modifierHtml);
                },
                error: function() {
                    console.log('Error in fetching modifiers');
                }
            });
        } else {
            $('#modifierInput').html('');
        }
    });
});
