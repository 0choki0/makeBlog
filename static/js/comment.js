console.log("comment 제대로 작동합니다.")

// comment create
let commentForms = document.querySelectorAll('.comment-Form')
commentForms.forEach(function(commentForm){    
    commentForm.addEventListener('submit', function(event){
        event.preventDefault()
        const data = new FormData(event.target)
        axios.post(event.target.action, data)
            .then(function(response){
            const comment = response.data
            const commentList = document.querySelector(
                `#comment-list-${comment.postId}`)
            const newComment = `
                ${comment.username} : ${comment.content}
                <i class="bi bi-heart comment_heart" data-post-id="${comment.postId}" data-comment-id="${comment.id}" onclick="comment_likeRequest(this, '${comment.postId}', '${comment.id}')">0명이 좋아합니다.</i>
                <button class="btn btn-light" onclick="commentDelete('${comment.postId},${comment.id}');">Delete</button>
            </div>`;
            commentList.insertAdjacentHTML('beforeEnd', newComment)
            event.target.reset()
        })
    })
})

// comment update
function commentUpdate(value) {
    var valuesArray = value.split(',')
    var comment_id = valuesArray[1];
    var post_id = valuesArray[0];
    var commentContent = $('.commentContent'+post_id+'-'+comment_id).val();
    // console.log(commentContent, valuesArray)

    $.ajax({
        type: 'POST',
        url: `/posts/${post_id}/comments/${comment_id}/update/`,
        dataType : 'json',
        data: {
            'comment_id': comment_id,
            'post_id': post_id,
            'comment_content': commentContent,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function(response) {
            $('#commentModal').modal('hide');
            location.reload();
        },
    });
}

// comment_delete
function commentDelete(value) {
    var valuesArray = value.split(',')
    var comment_id = valuesArray[1];
    var post_id = valuesArray[0];
    $.ajax({
        type : 'POST',
        url : `/posts/${post_id}/comments/${comment_id}/delete/`,
        dataType : 'json',
        data : {
            'comment_id': comment_id,
            'post_id': post_id,
            'csrfmiddlewaretoken': '{{csrf_token}}',
        },
        success: function(response){
            location.reload()
        }
    })
}

// comment like 
let comment_likeRequest = async (button, postId, commentId) => {
    let likeURL = `/posts/${postId}/comments/${commentId}/likes-async/`;
    try {
        let response = await fetch(likeURL);
        let result = await response.json();

        if (result.status) {
            button.classList.remove('bi-heart', 'comment_heart');
            button.classList.add('bi-heart-fill', 'comment_heart');
            button.style.color = 'red';
        } else {
            button.classList.remove('bi-heart-fill', 'comment_heart');
            button.classList.add('bi-heart', 'comment_heart');
            button.style.color = 'black';
        }

        button.innerHTML = result.count;
    } catch (error) {
        console.error('Error during like request:', error);
    }
};