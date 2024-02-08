console.log("reply 제대로 작동합니다.")

// reply form toggle
$('.replybutton').click(function(){
$(this).next('.replyform_div').toggle();
});    

// reply create
let replyForms = document.querySelectorAll('.reply-Form')
replyForms.forEach(function(replyForm){
    replyForm.addEventListener('submit', function(event){
        event.preventDefault()
        const data = new FormData(event.target)
        axios.post(event.target.action, data)
            .then(function(response){
            const reply = response.data
            const replyList = document.querySelector(
                `#reply-list-${reply.postId}-${reply.commentId}`)
            const newReply = `<div class="in">
                        ${ reply.username } : ${ reply.content }
                        <button onclick="replyDelete('${reply.postId},${reply.commentId},${reply.id}');">Delete</button>
                    </div>`
            replyList.insertAdjacentHTML('beforeEnd', newReply)
            event.target.reset()
            })
        })
    })


// reply_delete
function replyDelete(username, category, number, comment_id, reply_id) {
    $.ajax({
        type : 'POST',
        url : `/${username}/${category}/${number}/comments/${comment_id}/replys/${reply_id}/delete/`,
        dataType : 'json',
        data : {
            'username': username,
            'category': category,
            'number': number,
            'comment_id': comment_id,
            'reply_id' : reply_id,
            'csrfmiddlewaretoken': '{{csrf_token}}',
        },
        success: function(response){
            location.reload()
        }
    })
}

// reply_update
function replyUpdate(value) {
    var valuesArray = value.split(',')
    var reply_id = valuesArray[2];
    var comment_id = valuesArray[1];
    var post_id = valuesArray[0];
    var replyContent = $('.replyContent'+post_id+'-'+comment_id+'-'+reply_id).val();

    $.ajax({
        type: 'POST',
        url: `/posts/${post_id}/comments/${comment_id}/replys/${reply_id}/update/`,
        dataType : 'json',
        data: {
            'username': username,
            'category': category,
            'number': number,
            'comment_id': comment_id,
            'reply_id' : reply_id,
            'reply_content': replyContent,
            'csrfmiddlewaretoken': '{{ csrf_token }}',
        },
        success: function(response) {
            $('#replyModal').modal('hide');
            location.reload();
        },
    });
}
