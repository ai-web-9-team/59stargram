// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function register() {
    if (!checkNotEmpty(1)) {
        alert('이메일을 입력해주세요.')
        return;
    }
    if (!checkNotEmpty(2)) {
        alert('성명을 입력해주세요.')
        return;
    }
    if (!checkNotEmpty(3)) {
        alert('사용자이름을 입력해주세요.')
        return;
    }
    if (!checkNotEmpty(4)) {
        alert('비밀번호는 8자 이상 영문 대 소문자, 숫자, 특수문자를 사용하세요.')
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
        return $('#Name').val().length < 15 && $('#Name').val().length > 1
    }
    if (target == 3) {
        return $('#UserName').val().length < 15 && $('#UserName').val().length > 1
    }
    if (target == 4) {
        return $('#Password').val().length >= 8;
    }
}

  function id_overlap_check() {

    $('.username_input').change(function () {
      $('#id_check_sucess').hide();
      $('.id_overlap_button').show();
      $('.username_input').attr("check_result", "fail");
    })


    if ($('.username_input').val() == '') {
      alert('이메일을 입력해주세요.')
      return;
    }

    id_overlap_input = document.querySelector('input[name="username"]');

    $.ajax({
      url: "{% url 'lawyerAccount:id_overlap_check' %}",
      data: {
        'username': id_overlap_input.value
      },
      datatype: 'json',
      success: function (data) {
        console.log(data['overlap']);
        if (data['overlap'] == "fail") {
          alert("이미 존재하는 아이디 입니다.");
          id_overlap_input.focus();
          return;
        } else {
          alert("사용가능한 아이디 입니다.");
          $('.username_input').attr("check_result", "success");
          $('#id_check_sucess').show();
          $('.id_overlap_button').hide();
          return;
        }
      }
    });
  }