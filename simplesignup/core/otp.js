function send_otp() {
    $.ajax({
                url: "{% url 'ajax_send_otp' %}",
                type: "POST",
                data: { mobile_number:  $("#mobile_number").val() },
            })
            .done(function(data) {
                alert("OTP sent via SMS!");
            })
            .fail(function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown + ' : ' + jqXHR.responseText);
            });
}