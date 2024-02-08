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
                <button class="btn btn-light" onclick="commentDelete('${comment.postId},${comment.id}');">Delete</button>`;
            commentList.insertAdjacentHTML('beforeEnd', newComment)
            event.target.reset()
        })
    })
})

// comment update
function commentUpdate(username, category, number, comment_id) {
    $.ajax({
        type: 'POST',
        url: `/${username}/${category}/${number}/comments/${comment_id}/update/`,
        dataType : 'json',
        data: {
            'username': username,
            'category': category,
            'number': number,
            'comment_id': comment_id,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function(response) {
            $('#commentModal').modal('hide');
            location.reload();
        },
    });
}

// comment_delete
function commentDelete(username, category, number, comment_id) {
    $.ajax({
        type : 'POST',
        url : `/${username}/${encodeURIComponent(category)}/${number}/comments/${comment_id}/delete/`,
        dataType : 'json',
        data : {
            'username': username,
            'category': category,
            'number': number,
            'comment_id': comment_id,
            'csrfmiddlewaretoken': '{{csrf_token}}',
        },
        success: function(response){
            location.reload()
        }
    })
}

// comment like 
let comment_likeButtons = document.querySelectorAll("i.comment_heart")

comment_likeButtons.forEach((comment_likeButton)=>{            
    comment_likeButton.addEventListener("click", (event)=>{
        let postId = event.target.dataset.postId
        let commentId = event.target.dataset.commentId 
        let username = event.target.closest(".btn").dataset.username
        let category = event.target.closest(".btn").dataset.category 
        comment_likeRequest(event.target, postId, username, category, commentId)
    })
})

let comment_likeRequest = async (button, postId, username, category, commentId) => {
    let comment_likeURL = `/${username}/${category}/${postId}/comments/${commentId}/likes-async/`;
    try {
        let response = await fetch(comment_likeURL);
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