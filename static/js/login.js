function login() {
    if (!checkNotEmpty(1)) {
        alert('없는 이메일 입니다.')
        return;
    }
    if (!checkNotEmpty(2)) {
        alert('비밀번호가 일치하지 않습니다.')
        return;
    }
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: {id_give: $('#Email').val(), pw_give: $('#Password').val()},
        success: function (response) {
            if (response['result'] === 'success') {
                alert(response['msg']),
                    $.cookie('token', response['token'])
                window.location.href = '/index';
            } else {
                alert(response['msg'])
            }
        }
    })
}

function checkNotEmpty(target) {

    if (target == 1) {
        return $('#Email').val().length > 10;
    }
    if (target == 2) {
        return $('#Password').val().length >= 8;
    }
}

// function checkNotEmpty() {
//     return $('#Password').val().length >= 8 && $('#Email').val().length > 0;
// }
