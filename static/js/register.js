// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function register() {

    // 회원가입 판단 (코드들__
    // 회원가입 가능하면
    //$.ajax()

    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: $('#Email').val(),
            pw_give: $('#Password').val(),
            pwd2: $('#PasswordCheck').val(),
            nickname_give: $('#UserName').val(),
            name_give: $('#Name').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login'
            } else {
                alert(response['msg'])
            }
        }
    })

}

$('.pw').focusout(function () {
    var pwd1 = $("#Password").val();
    var pwd2 = $("#PasswordCheck").val();

    if (pwd1 != '' && pwd2 == '') {
    } else if (pwd1 != "" || pwd2 != "") {
        if (pwd1 == pwd2) {
            $("#alert-success").css('display', 'inline-block');
            $("#alert-danger").css('display', 'none');
        } else {
            $("#alert-success").css('display', 'none');
            $("#alert-danger").css('display', 'inline-block');
        }
    }
});

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

