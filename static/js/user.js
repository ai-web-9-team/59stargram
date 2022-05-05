// 사용자 페이지 로딩시 posts 탭을 보여줌
$(document).ready(function () {
    user_menu_on('posts')
})

// 메뉴 클릭시 클릭한 메뉴 활성화
// name : 클릭한 메뉴 태그의 name
function user_menu_on(name){
    $('.user_posts_menu').css('border-top', '1px solid #e8e8e8');
    $('.user_posts_menu').css('font-weight', '300');
    $('.user_posts_menu').css('opacity', '0.5');

    $(`.user_posts_menu[name=${name}]`).css('border-top', '2px solid black');
    $(`.user_posts_menu[name=${name}]`).css('font-weight', 'bold');
    $(`.user_posts_menu[name=${name}]`).css('opacity', '1');
}