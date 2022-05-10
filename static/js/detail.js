
//  일단 첫번째 피드만...  about_post의 내용 누르면 그 위에 상세페이지 모달창 나오기
const modal1 = document.getElementById("modal_overlay");
const clickmodal1 = document.getElementById("about_post");
clickmodal1.addEventListener("click", e => {
    modal1.style.top = window.scrollY + 'px';
    modal1.style.display = "flex";
    document.body.style.overflowY = "hidden";

    // 1. post_id 가져와서
    let post_id = $('#about_post').attr('name')

    // 2. post_id 보내주기
    // 4. post 정보 받기
    // 5. 원하는 곳에 넣기
    $.ajax({
        type: "GET",
        url: '/details?post_id=' + post_id,
        data: {},
        success: function (response) {
            let user_name = response['new_post']['UserName']
            $('#modal_user_name').text(user_name)

            let description = response['new_post']['Description']
            $('#modal_img_description').text(description)

            let date = response['new_post']['Date']
            $('#modal_date').text(date)

            let likecnt = response['new_post']['LikeCnt']
            $('#modal_img_description').text(description)
        }
    })
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






