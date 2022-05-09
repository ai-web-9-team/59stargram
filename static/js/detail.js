
//  일단 첫번째 피드만...  about_post의 내용 누르면 그 위에 상세페이지 모달창 나오기
const modal1 = document.getElementById("modal_overlay");
const clickmodal1 = document.getElementById("about_post");
clickmodal1.addEventListener("click", e => {
    modal1.style.top = window.scrollY + 'px';
    modal1.style.display = "flex";
    document.body.style.overflowY = "hidden";
});


const CloseModal1 = document.getElementById("close_btn");
CloseModal1.addEventListener("click", e => {
    modal1.style.display = "none";
    document.body.style.overflowY = "visible";
});


// 댓글입력시 게시글밑에 달리기

const commentInput = document.getElementById("commentInput");
const commentSubmit = document.getElementById("submit")

function checkInput() {
    const newComment = commentInput.value;
    if (newComment.length > 0) { // input의 값이 0 보다 클때
        addComment(newComment); // addComment함수를 실행한다.
    } else if (window.event.code === 'Enter') { // 엔터를 입력하면
        if (newComment.length > 0) { // input의 값이 0보다 클때
            addComment(newComment);// addComment함수를 실행한다.
        } else { // 0 보다 작을 때
            alert("댓글을 입력하세요!");// alert 창을 띄워준다.
        }
    } else { // input 의 값이 0보다 작을 때
        alert("댓글을 입력하세요!");// alert 창을 띄워준다.
    }
    event.preventDefault(); // 이벤트를 취소 해 준다.
}


function addComment(value) {
    const commentLists = document.getElementById('comment-wrapper');
    const newCommentList = document.createElement('li');
    const defaultComment = `<li class="modal_comment_list">
                                <span class="modal_profile_img_round">사진</span>
                                <span class="modal_user_name">유저 아이디</span>
                                <span> ${value}</span>
                                <button class="delete"> 삭제 </button>
                                <span>🤍</span>
                            </li>`

    newCommentList.innerHTML = defaultComment; // li 태그에 댓글default값을 설정 해 준다.
    commentLists.appendChild(newCommentList);// ul에 li 를 자식요소로 붙인다.
    commentInput.value = ""; // 댓글 입력 후 input의 값을 비어있게 만든다.

    deleteComment(newCommentList);// deleteComment 함수를 실행시킨다.
}


function deleteComment(newCommentList) {
    const deleteBtn = newCommentList.querySelector('.delete');
    deleteBtn.addEventListener('click', () => newCommentList.remove());
}


const init = () => {
    commentSubmit.addEventListener('click', checkInput);
}

init();





// 현재 시간과 비교해서 글쓴 시간 계산
timeBefore();

function timeBefore() {
    //현재시간
    var now = new Date();
    console.log(now);
    //글쓴 시간
    var writeDay = new Date('Wen April 20 2022 15:01:17 GMT+0900');
    var minus;
    if (now.getFullYear() > writeDay.getFullYear()) {
        minus = now.getFullYear() - writeDay.getFullYear();
        document.getElementsByClassName("sub")[0].innerHTML = minus + "년 전";
        console.log(minus + "년 전");
    } else if (now.getMonth() > writeDay.getMonth()) {
        minus = now.getMonth() - writeDay.getMonth();
        document.getElementsByClassName("sub")[0].innerHTML = minus + "달 전";
        console.log(minus + "달 전");
    } else if (now.getDate() > writeDay.getDate()) {
        minus = now.getDate() - writeDay.getDate();
        document.getElementsByClassName("sub")[0].innerHTML = minus + "일 전";
        console.log(minus + "일 전");
    } else if (now.getDate() == writeDay.getDate()) {
        var nowTime = now.getTime();
        var writeTime = writeDay.getTime();
        if (nowTime > writeTime) {
            sec = parseInt(nowTime - writeTime) / 1000;
            day = parseInt(sec / 60 / 60 / 24);
            sec = (sec - (day * 60 * 60 * 24));
            hour = parseInt(sec / 60 / 60);
            sec = (sec - (hour * 60 * 60));
            min = parseInt(sec / 60);
            sec = parseInt(sec - (min * 60));
            if (hour > 0) {
                document.getElementsByClassName("sub")[0].innerHTML = hour + "시간 전";
                console.log(hour + "시간 전");
            } else if (min > 0) {
                document.getElementsByClassName("sub")[0].innerHTML = min + "분 전";
                console.log(min + "분 전");
            } else if (sec > 0) {
                document.getElementsByClassName("sub")[0].innerHTML = sec + "초 전";
                console.log(sec + "초 전");
            }
        }
    }
}


