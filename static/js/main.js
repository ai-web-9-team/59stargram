function fadeOut(id) {
    var like_button_id = "like_button" + id.substring(5,);
    document.getElementById(like_button_id).style.color = 'red';
    document.getElementById(id).style.opacity = 0.3;
    setTimeout(function () {
        document.getElementById(id).style.opacity = 1;
        document.getElementById("carouselExampleControls").style.opacity = 1;
    }, 400);
}

//하트 이모티콘을 누르면 호출되는 함수
function clickLike(id) {
    if (document.getElementById(id).style.color != 'red') { // 빨간색이 아니면 (눌린 상태가 아니면)
        document.getElementById(id).style.color = 'red'; // 좋아요 표시
    } else { // 빨간색이면
        document.getElementById(id).style.color = 'black'; //좋아요 취소
    }
}

// 책갈피 이모티콘을 누르면 호출되는 함수
function clickBookmark(id) {
    if (document.getElementById(id).style.color != 'red') {
        document.getElementById(id).style.color = 'red';
    } else {
        document.getElementById(id).style.color = 'black';
    }
}

// 스토리 클릭 시 해당 게시글 offset으로 스크롤 이동하는 함수
function clickStory(id) {
    var story_id = "#" + id;
    var feed_id = "#feed" + id.substring(5,);
    var offset = $(feed_id).offset();
    $('html').animate({scrollTop: offset.top - 90}, 800);
}

// 검색창에 추천 검색어 띄우는 모달창
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
});


const body = document.querySelector('body');
const more_outside = document.querySelector('.more_button_box');
const alert_outside = document.querySelector('.alert_button_box');
const add_feed_outside = document.querySelector('.add_feed_box');

// type 0: 내 게시물 더보기 창, 1: 팔로우 중인 사람의 게시물 더보기 창, 2: 팔로우 중이 아닌 사람의 게시물 더보기 창
function more_button_on(type) {
    if (type == 0) {
        $('.card-header1').text("게시물 수정");
        $('.card-header2').text("게시물 삭제");
        $('.card-header3').text("게시물 공유");
        $('.card-header4').text("게시물 저장");
    } else if (type == 1) {
        $('.card-header1').text("해당 유저 페이지로 이동");
        $('.card-header2').text("해당 유저 팔로우 취소");
        $('.card-header3').text("게시물 공유");
        $('.card-header4').text("게시물 저장");
    } else if (type == 2) {
        $('.card-header1').text("해당 유저 페이지로 이동");
        $('.card-header2').text("해당 유저 팔로우");
        $('.card-header3').text("게시물 공유");
        $('.card-header4').text("게시물 저장");
    }
    more_outside.classList.toggle('show');
    if (more_outside.classList.contains('show')) {
        body.style.overflow = 'hidden';
    }
}

function alert_button_on() {
    $('.card-header1').text("ㅇㅇㅇ이 게시물에 좋아요를 눌렀습니다.");
    $('.card-header2').text("ㅇㅇㅇ이 게시물에 댓글을 달았습니다.");
    $('.card-header3').text("ㅇㅇㅇ이 게시물에 댓글을 달았습니다.");
    $('.card-header4').text("ㅇㅇㅇ이 게시물에 댓글을 달았습니다.");
    $('.card-header5').text("ㅇㅇㅇ이 게시물에 댓글을 달았습니다.");
    alert_outside.classList.toggle('show');
    if (alert_outside.classList.contains('show')) {
        body.style.overflow = 'hidden';
    }
}

function add_feed_on() {
    add_feed_outside.classList.toggle('show');
    if (add_feed_outside.classList.contains('show')) {
        body.style.overflow = 'hidden';
    }
}


// 모달창 사라지기
function more_button_quit() {
    more_outside.classList.toggle('show');

    if (!more_outside.classList.contains('show')) {
        body.style.overflow = 'auto';
    }
}

function alert_button_quit() {
    alert_outside.classList.toggle('show');

    if (!alert_outside.classList.contains('show')) {
        body.style.overflow = 'auto';
    }
}

function add_feed_quit() {
    add_feed_outside.classList.toggle('show');

    if (!add_feed_outside.classList.contains('show')) {
        body.style.overflow = 'auto';
    }
}


// 모달 밖을 클릭하면 모달창 닫기
more_outside.addEventListener('click', (event) => {
    if (event.target === more_outside) {
        more_button_quit();
    }
});

alert_outside.addEventListener('click', (event) => {
    if (event.target === alert_outside) {
        alert_button_quit();
    }
});

add_feed_outside.addEventListener('click', (event) => {
    if (event.target === add_feed_outside) {
        add_feed_quit();
    }
});

function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href = '/login'
}