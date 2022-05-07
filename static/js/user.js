// 사용자 페이지 로딩시 posts 탭을 보여줌
$(document).ready(function () {
    user_menu_on('posts')
})

// 메뉴 클릭시 클릭한 메뉴 활성화
// name : 클릭한 메뉴 태그의 name
function user_menu_on(name){
    $('.user_post_menu').css('border-top', '1px solid #e8e8e8');
    $('.user_post_menu').css('font-weight', '300');
    $('.user_post_menu').css('opacity', '0.5');

    $(`.user_post_menu[name=${name}]`).css('border-top', '2px solid black');
    $(`.user_post_menu[name=${name}]`).css('font-weight', 'bold');
    $(`.user_post_menu[name=${name}]`).css('opacity', '1');
}

const body = document.querySelector('body');
const modal_outside = document.querySelector('.user_follower_box');


// 팔로우 모달 API 전달하기
// type - 0:팔로워, 1:팔로잉
function user_modal_on(type) {

    console.log(type);

    let title_text;
    if (type == 0) {
        title_text = '팔로워';
    } else if (type == 1) {
        title_text = '팔로잉';
    } else {
        return;
    }

    $('.user_follower_title_text').text(title_text);

    modal_outside.classList.toggle('show');
    if (modal_outside.classList.contains('show')) {
        body.style.overflow = 'hidden';
    }
}



// 모달 밖을 클릭하면 모달창 사라지기
function user_modal_quit() {
    modal_outside.classList.toggle('show');

  if (!modal_outside.classList.contains('show')) {
    body.style.overflow = 'auto';
  }
}


modal_outside.addEventListener('click', (event) => {
if (event.target === modal_outside) {
    user_modal_quit()
}
});