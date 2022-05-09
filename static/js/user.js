// 사용자 페이지 로딩시 posts 탭을 보여줌
$(document).ready(function () {
    user_menu_on('posts')

    // 유저 요약 모달창 이벤트
    $(`.user_follower_username`).hover(function () {
        let name = $(this).attr('name')
        let top = $(this).offset().top;
        let left = $(this).offset().left;
        user_summary_modal_on(name, top, left)
    }, function () {
        user_modal_quit(1);
    });

    $('.user_post_img_box').hover(function () {
        $(this).children('.user_post_info_box').css('display', 'block')
    }, function () {
            $(this).children('.user_post_info_box').css('display', 'none')
    })
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
const modal_follow_outside = document.querySelector('.user_follower_box');
const modal_summary_outside = document.querySelector('.user_summary_body');
const modal_setting_outside = document.querySelector('.user_setting_modal_box');

// 팔로우 모달 API 전달하기
// type - 0:팔로워, 1:팔로잉
function user_follow_modal_on(type) {
    let title_text;
    if (type == 0) {
        title_text = '팔로워';
    } else if (type == 1) {
        title_text = '팔로잉';
    } else {
        return;
    }

    $('.user_follower_title_text').text(title_text);

    modal_follow_outside.classList.toggle('show');
    if (modal_follow_outside.classList.contains('show')) {
        body.style.overflow = 'hidden';
    }
}

// 유저 요약 모달 API 전달하기
function user_summary_modal_on(name, top, left) {
    let offset_top = $('.user_follower_body').offset().top + top
        + 50
    let offset_left = $('.user_follower_body').offset().left + left + 50

    offset_top = parseInt(offset_top).toString()+'px'
    offset_left = parseInt(offset_left).toString()+'px'

    modal_summary_outside.style.top = offset_top
    modal_summary_outside.style.left = offset_left

    modal_summary_outside.classList.toggle('show');
}

// 유저 설정 모달 API 전달하기
function user_setting_modal_on() {
    modal_setting_outside.classList.toggle('show');
    if (modal_setting_outside.classList.contains('show')) {
        body.style.overflow = 'hidden';
    }
}


// 모달창 사라지기
// type - 0:팔로우 모달창, 1:유저요약 모달창, 2:유저설정 모달창
function user_modal_quit(type) {
    if (type == 0) {
        modal_follow_outside.classList.toggle('show');

        if (!modal_follow_outside.classList.contains('show')) {
            body.style.overflow = 'auto';
        }
    } else if (type == 1) {
        modal_summary_outside.classList.toggle('show');
    } else if (type == 2) {
        modal_setting_outside.classList.toggle('show');

        if (!modal_setting_outside.classList.contains('show')) {
            body.style.overflow = 'auto';
        }

    } else {
        return;
    }
}

// 모달 밖을 클릭하면 모달창 닫기
modal_follow_outside.addEventListener('click', (event) => {
    if (event.target === modal_follow_outside) {
        user_modal_quit(0)
    }
});
modal_setting_outside.addEventListener('click', (event) => {
    if (event.target === modal_setting_outside) {
        user_modal_quit(2)
    }
});

// 유저