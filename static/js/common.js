// 검색창 활성화시키는 함수
function active_search_input_box() {
    $('#search_icon').css("display", "none")
    $('#search_active_button').css("display", "none")
    $('#search_input_box').css("width", "90%")
    $('#search_input_box').focus()
}

// profile 마진값 계산하는 함수
function update_profile_margin() {
    let screen_width = $(window).width()
    let self_width = $('#main_body').width()
    let margin = screen_width - self_width
    let margin_right = (margin / 2).toString()

    let str = margin_right + "px"
    $('#profile_box').css("right", str)
}

// 스토리 슬라이드 함수
// vector : 슬라이드 방향 - 0:왼쪽, 1:오른쪽
function move_story_slide(vector) {
    let margin_text = $('#stories').css('margin-left')
    let width_text = $('#stories').css('width')
    let box_text = $('#card').css('width')

    let margin_num = Number(margin_text.slice(0, -2))
    let width_num = Number(width_text.slice(0, -2))
    let box_num = Number(box_text.slice(0, -2))

    let max_margin = 0  // 최대 마진 값
    let move_margin = 150   // 한번 이동할 때 움직일 마진 값

    if (width_num > box_num) {
        max_margin = width_num - box_num
    }

    if (vector == 1) {
        if (margin_num == 0) {
            $('#bg_slide_button_left').css("opacity", "1")
            $('#bg_slide_button_left').css("display", "block")
        }
        margin_num = margin_num - move_margin
        if (margin_num < -1 * max_margin) {
            margin_num = -1 * max_margin
            $('#bg_slide_button_right').css("opacity", "0")
            $('#bg_slide_button_right').css("display", "none")
        }
    } else {
        if (margin_num == -1 * max_margin) {
            $('#bg_slide_button_right').css("opacity", "1")
            $('#bg_slide_button_right').css("display", "block")
        }
        margin_num = margin_num + move_margin
        if (margin_num > 0) {
            margin_num = 0
            $('#bg_slide_button_left').css("opacity", "0")
            $('#bg_slide_button_left').css("display", "none")
        }
    }
    let update_margin = (margin_num).toString() + "px"

    $('#stories').css('margin-left', update_margin)
}

// 포스트 텍스트 더보기 버튼 함수
function view_post_text_more(name) {
    $(`.post_text_btn[name=${name}]`).css('display', 'none')
    $(`.post_text_more[name=${name}]`).css('display', 'block')
}

// 로딩시 profile 마진값 다시 계산
$(document).ready(function () {
    update_profile_margin()
})

$(function () {
    // 검색창에서 focus를 다른 곳으로 옮길 때
    $('#search_input_box').blur(()=>{
        $('#search_icon').css("display", "block")
        $('#search_active_button').css("display", "block")
        $('#search_input_box').css("width", "70%")
    })


    // 화면 사이즈 변경 시
    // profile 마진값 다시 계산
    $(window).resize(function () {
        update_profile_margin()
    });

    // 현재 선택된 댓글창에 상태에 따라 게시 버튼 효과 변경
    $('.post_comment_input').on('focus blur keyup', () => {
        let name = $(':focus').attr('name');

        if ($(`.post_comment_input[name='${name}']`).val() === "") {
            $(`.post_comment_input_btn[name='${name}']`).css('opacity', '0.5')
        } else {
            $(`.post_comment_input_btn[name='${name}']`).css('opacity', '1')
        }
    })
});

function fadeOut(id) {
                    var like_button_id="like_button"+id.substring(5, );
                    document.getElementById(like_button_id).style.color='red';
                    document.getElementById(id).style.opacity=0.3;
                    setTimeout(function() { document.getElementById(id).style.opacity=1;
                    document.getElementById("carouselExampleControls").style.opacity=1;}, 400);
                }

//하트 이모티콘을 누르면 호출되는 함수
function clickLike(id) {
                            if (document.getElementById(id).style.color != 'red') { // 빨간색이 아니면 (눌린 상태가 아니면)
                                document.getElementById(id).style.color='red'; // 좋아요 표시
                            }
                            else { // 빨간색이면
                                document.getElementById(id).style.color='black'; //좋아요 취소
                            }
                        }

// 책갈피 이모티콘을 누르면 호출되는 함수
function clickBookmark(id) {
                            if (document.getElementById(id).style.color != 'red') {
                                document.getElementById(id).style.color='red';
                            }
                            else {
                                document.getElementById(id).style.color='black';
                            }
                        }


// 모달 창을 띄우는 함수 (뒷 배경을 흐릿흐릿하게 하는 것도 이곳에서 처리)
function openModal(id) {
    var zIndex=9999;
    var modal=document.getElementById(id);
    var bg = document.createElement('div');


    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        backgroundColor: 'rgba(0,0,0,0.5)'
    });

    document.body.append(bg);
    modal.querySelector('.modal_close_btn').addEventListener('click', function() {
        bg.remove();
        modal.style.display = 'none';
    });

    //var top_offset=document.querySelector('#feed1').offsetTop;
    //console.log(top_offset);
    // var left_offset=document.querySelector('#feed1').offsetTop;
    modal.setStyle({
        position: 'fixed',
        display: 'block',
        boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',

        // 시꺼먼 레이어 보다 한칸 위에 보이기
        zIndex: zIndex + 1,

        // div center 정렬
        top: '50%',
        left: '43%',
        transform: 'translate(-50%, -50%)',
        msTransform: 'translate(-50%, -50%)',
        webkitTransform: 'translate(-50%, -50%)'
    });
}

Element.prototype.setStyle = function(styles) {
    for (var k in styles) this.style[k] = styles[k];
    return this;
};

// 자신의 게시글의 더보기 버튼을 누르면 호출되는 함수
function moreMyPost() {
    // 모달창 띄우기
    openModal("more_button_me");
}

// 팔로우 중인 사람의 게시글의 더보기 버튼을 누르면 호출되는 함수
function moreFollowPost() {
    // 모달창 띄우기
    openModal("more_button_follow");
}

// 팔로우 중이 아닌 사람의 게시글의 더보기 버튼을 누르면 호출되는 함수
function moreNotFollowPost() {
    // 모달창 띄우기
    openModal("more_button_not_follow");
}

// 스토리 클릭 시 해당 게시글 offset으로 스크롤 이동하는 함수
function clickStory(id) {
    var story_id = "#"+id;
    var feed_id = "#feed"+id.substring(5, );
    var offset = $(feed_id).offset();
    $('html').animate({scrollTop : offset.top-90}, 800);
}


const inputBox = document.getElementById("search_input_box");
const recommendBox = document.querySelector("#search_recommend");
const texts = document.querySelectorAll(".text");

inputBox.addEventListener("keyup", (e) => {
	if (e.target.value.length > 0) {
		recommendBox.classList.remove('invisible');
		texts.forEach((textEl) => {
			textEl.textContent = e.target.value;
		})
	} else {
		recommendBox.classList.add('invisible');
	}
})
