function login() {


    $.ajax({
        type: "POST",
        url: "/api/login",
        data: {
            id_give: $('#Email').val(),
            pw_give: $('#Password').val(),

        },
        success: function (response) {
            if (response['result'] === 'success') {
                alert(response['msg']),
                    $.cookie('mytoken', response['token'])
                window.location.href = '/';
            } else {
                alert(response['msg'])
            }
        }
    })
}

function emailform(obj) {
    if (emailformCheck(obj) == false) {
        alert('올바른 이메일 주소를 입력해주세요.')
        obj.value = '';
        obj.focus();
        return false;
    }
}

function emailformCheck(obj) {
    var pattern = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
    return (obj.value.match(pattern) != null)
}

function passwordform(obj) {
    if (passwordformCheck(obj) == false) {
        alert('비밀번호는 8글자 이상의 영문, 숫자로 작성해주세요.')
        obj.value = '';
        obj.focus();
        return false;
    }
}

function passwordformCheck(obj) {
    var pattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/i;
    return (obj.value.match(pattern) != null)
}