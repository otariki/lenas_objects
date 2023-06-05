$(document).ready( function () {
    ///////////////////////////////////////////////// reg       START
    if( $("#reg_get_param__err").text() != "None" && $("#reg_get_param__err").text() != "" ) {
        if ($("#reg_get_param__err").text() == "1") {
            alert("თქვენ დარეგისტრირდით წარმატებით, თუმცა აუცილებელია იმეილის აქტივაცია, თქვენს მიერ მითითებულ იმეილზე გამოიგზავნება წერილი რამოდენიმე წუთში, გთხოვთ ნახოთ და მიჰყვეთ ინსტრუქციას");
        }
//        if ($("#reg_get_param__err").text() == "pass_changed") {
//            alert("პაროლი წარმატებით შეიცვალა, შეგიძლიათ ავტორიზება");
//        }

    }

    $('#show_pass').on('change', function() {
        var checked = this.checked;
        if (checked) {
            //alert("machvene");
            $(".pass_fields").attr('type', 'text');
        }
        else {
            $(".pass_fields").attr('type', 'password');
        }
    });

    $("#reg_btn").on("click", function() {
        v_reg_code = $("#reg_code").val().trim();
        v_user_name = $("#user_name").val().trim();
        v_email = $("#email").val().trim();
        v_pass = $("#pass").val().trim();
        v_pass2 = $("#pass2").val().trim();



        if (v_reg_code.length != 9) {
            alert("რეგისტრაციის კოდი არასწორია");
            return false;
        }

        if (v_user_name.length < 2) {
            alert("მომხმარებლის სახელი უნდა შეიცავდეს მინიმუმ 2 სიმბოლოს");
            return false;
        }

        var mail_regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (v_email.match(mail_regex) == false || v_email.match(mail_regex) == null) {
            alert("შეიყვანეთ რეალური იმეილი");
            return false;
        }




        if (v_pass.length < 8) {
            alert("პაროლი უნდა იყოს 8 ან მეტი სიმბოლო");
            return false;
        }
        var pass_regex1 = /[0-9]+/;
        var pass_regex2 = /[A-Z]+/;
        var pass_regex3 = /[a-z]+/;
        if (v_pass.match(pass_regex1) == null || v_pass.match(pass_regex2) == null || v_pass.match(pass_regex3) == null) {
            alert("პაროლი უნდა შეიცავდეს მინიმუნ ერთ ციფრს, ერთ დიდ და ერთ პატარალა ლათინურ სიმბოლოს");
            return false;
        }
        if (v_pass != v_pass2) {
            alert("გაიმოეროეთ პაროლი სწორად");
            return false;
        }

        data_for_send = {
            "email": v_email,
            "user_name": v_user_name
        }

        $.ajax({
            headers: { "X-CSRFToken": $("#csrf").text() },
            url: $("#reg_aj_url").text(),
            type: 'post',
            data: data_for_send,
            success: function(resp) {
                console.log( resp );
                // resp.msg
                if (resp.res == "success"){
                    $("#reg_form").submit();
                }
                else if (resp.res == "error_2") {
                    alert("ასეთი იმეილი უკვე რეგისტრირებულია, გთხოვთ გამოიყენოთ სხვა იმეილი");
                    return false;
                }
                else if (resp.res == "error_3") {
                    alert("ასეთი მომხმარებლის სახელი უკვე რეგისტრირებულია, გთხოვთ გამოიყენოთ სხვა სახელი");
                    return false;
                }
            }
        });


    });
    ///////////////////////////////////////////////// reg       END



    ///////////////////////////////////////////////// auth     START
    if( $("#auth_get_param__msg").text() != "None" && $("#auth_get_param__msg").text() != "" ) {
        if ($("#auth_get_param__msg").text() == "email_confirmed") {
            alert("იმეილის აქტივაცია წარმატებულია, შეგიძლიათ ავტორიზება");
        }
        if ($("#auth_get_param__msg").text() == "pass_changed") {
            alert("პაროლი წარმატებით შეიცვალა, შეგიძლიათ ავტორიზება");
        }

    }
    if($("#auth_get_param__err").text() != "None" && $("#auth_get_param__err").text() != "") {
        if ($("#auth_get_param__err").text() == "no_user_found_4") {
            alert('თქვენ რეგისტრირებული ხართ, მაგრამ იმეილი არა აქტივირებულია. გასააქტიურებლად დააკლიკეთ "იმეილის აქტივაცია"');
        }
        else {
            alert('ავტორიზაცია ვერ მოხერხდა');
        }
    }

    if ($("#email_activation_link").data("email") != "") {
        $("#email_activation_link").css({"display":"block"});
    }
    $("#email_activation_link").on("click", function () {
        v_email = $(this).data("email");

        data_for_send = {
            "email": v_email
        }

        $.ajax({
            headers: { "X-CSRFToken": $("#csrf").text() },
            url: $("#aj_send_email_activation_code").text(),
            type: 'post',
            data: data_for_send,
            success: function(resp) {
                console.log( resp.res );
                if (resp.res == "success") {
                    alert("იმეილზე "+v_email+" გამოიგზავნა აქტივაციის კოდი, გთხოვთ ნახოთ მეილი და მიჰყვეთ ინსტრუქციას");
                } else {
                    alert("იმეილის აქტივაციის კოდი ვერ გამოიგზავნა");
                }


            }
        });

    });



    $("#auth_btn").on("click", function() {
        v_email = $("#email").val();
        v_pass = $("#pass").val();

        var mail_regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (v_email.match(mail_regex) == false || v_email.match(mail_regex) == null) {
            alert("შეიყვანეთ რეალური იმეილი");
            return false;
        }

        if (v_pass.length < 8) {
            alert("პაროლი არასწორია");
            return false;
        }
        var pass_regex1 = /[0-9]+/;
        var pass_regex2 = /[A-Z]+/;
        var pass_regex3 = /[a-z]+/;
        if (v_pass.match(pass_regex1) == null || v_pass.match(pass_regex2) == null || v_pass.match(pass_regex3) == null) {
            alert("პაროლი არასწორია");
            return false;
        }


        $("#auth_form").submit();
    });
    ///////////////////////////////////////////////// auth     END


    ///////////////////////////////////////////////// change password       START
    if( $("#cp_send_email_get_param__msg").text() != "None" && $("#cp_send_email_get_param__msg").text() != "" ) {
        if ($("#cp_send_email_get_param__msg").text() == "email_sended") {
            alert("მეილი გამოგზავნილია, გთხოვთ შეამოწმოთ და მიჰყვეთ ინქტრუქციას");
        }
//        if ($("#cp_send_email_get_param__msg").text() == "pass_changed") {
//            alert("პაროლი წარმატებით შეიცვალა, შეგიძლიათ ავტორიზება");
//        }

    }


    $("#change_pass_send_email_btn").on("click", function() {
        v_email = $("#email").val().trim();
        var mail_regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (v_email.match(mail_regex) == false || v_email.match(mail_regex) == null) {
            alert("შეიყვანეთ რეალური იმეილი");
            return false;
        }

        $("#change_pass_send_email_form").submit();
    });

    $("#change_pass_btn").on("click", function() {
        v_pass = $("#pass").val().trim();
        v_pass2 = $("#pass2").val().trim();

        if (v_pass.length < 8) {
            alert("პაროლი უნდა იყოს 8 ან მეტი სიმბოლო");
            return false;
        }
        var pass_regex1 = /[0-9]+/;
        var pass_regex2 = /[A-Z]+/;
        var pass_regex3 = /[a-z]+/;
        if (v_pass.match(pass_regex1) == null || v_pass.match(pass_regex2) == null || v_pass.match(pass_regex3) == null) {
            alert("პაროლი უნდა შეიცავდეს მინიმუნ ერთ ციფრს, ერთ დიდ და ერთ პატარალა ლათინურ სიმბოლოს");
            return false;
        }
        if (v_pass != v_pass2) {
            alert("გაიმეორეთ პაროლი სწორად");
            return false;
        }

        $("#change_pass_form").submit();
    });
    ///////////////////////////////////////////////// change password       END


});