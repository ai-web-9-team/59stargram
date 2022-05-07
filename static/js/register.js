// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function register() {
    if (!checkNotEmpty(1)) {
        alert('이메일을 입력해')
        return;
    }
    if (!checkNotEmpty(2)) {
        alert('2')
        return;
    }
    if (!checkNotEmpty(3)) {
        alert('3')
        return;
    }
    if (!checkNotEmpty(4)) {
        alert('8자 이상 영문 대 소문자, 숫자를 사용하세요.')
        return;
    }
    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {
            id_give: $('#Email').val(),
            pw_give: $('#Password').val(),
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

function checkNotEmpty(target) {

    if (target == 1) {
        return $('#Email').val().length > 10;
    }
    if (target == 2) {
        return $('#Name').val().length < 15 && $('#Name').val().length >1
    }
    if (target == 3) {
        return $('#UserName').val().length < 15 && $('#UserName').val().length > 1
    }
    if (target == 4) {
        return $('#Password').val().length >= 8;
    }
}

// function checkNotEmpty() {
//     return $('#Password').val().length >= 8 && $('#Email').val().length > 0 && $('#UserName').val().length < 15 && $('#Name').val().length < 15;
// }
