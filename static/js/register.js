// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function register() {
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

function emailform(obj) {
    if(emailformCheck(obj)==false){
        alert('올바른 이메일 주소를 입력해주세요.')
        obj.value='';
        obj.focus();
        return false;
    }
}

function emailformCheck(obj){
    var pattern = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
    return (obj.value.match(pattern)!=null)
}
