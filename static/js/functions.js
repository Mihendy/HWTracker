async function make_request(method, url, data) {
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
    })
    if (response.ok) {
        return response
    } else {
        let error = new Error('Error occurred during the fetch request.');
        console.error('ERROR: ', error);
        throw error
    }
}

function recountRows() {
    let rows = document.getElementsByClassName('group-row');
    for (let i = 0; i < rows.length; i++) {
        let counterCell = rows[i].getElementsByClassName('counter')[0];
        counterCell.textContent = i + 1;
    }
}

async function checkTask(element, task_id, status, user_id) {
    const response = await make_request('POST', '/checktask/', {
        task_id: task_id,
        status: status,
        user_id: user_id,
    });

    const data = await response.json();
    if (data.success) {
        element.classList.toggle('selected-card');
        if (status === 'completed') {
            element.setAttribute('onclick', "checkTask(this, " + task_id + ", 'incompleted', " + user_id + ");");
        } else {
            element.setAttribute('onclick', "checkTask(this, " + task_id + ", 'completed', " + user_id + ");");
        }
    }
    // console.log(data);
    return data;
}

async function deleteTaskBlock(taskId) {
    const response = await make_request('POST', '/deletetask/', {
        task_id: taskId,
    });
    const data = await response.json();
    if (data.success) {
        const taskBlock = document.getElementById(taskId);
        const tasksBox = taskBlock.parentElement;
        // console.log(tasksBox)
        if (tasksBox.childElementCount === 1) {
            tasksBox.parentElement.remove();
        }
        taskBlock.remove();
    }
    // console.log(data);
    return data;
}

async function deleteGroup(groupId) {
    const response = await make_request('POST', '/deletegroup/', {
        group_id: groupId,
    });
    const data = await response.json();
    if (data.success) {
        const groupBlock = document.getElementById(groupId);
        groupBlock.remove();
        recountRows();
    }
    // console.log(data);
    return data;
}

async function deleteUser(userId) {
    const response = await make_request('POST', '/deleteuser/', {
        user_id: userId,
    });
    const data = await response.json();
    if (data.success) {
        const userBlock = document.getElementById(userId);
        userBlock.remove();
        recountRows();
    }
    // console.log(data);
    return data;
}

async function createDeletePostModalView(postID) {
    let confirmationText = document.querySelector('.confirmation-text')
    let postCard = document.getElementById(postID)
    let postTitle = postCard.querySelector('.card-title').textContent
    confirmationText.innerHTML = `Вы действительно хотите удалить статью "${postTitle}"? Это действие <b>необратимо</b>.`
    let postDeleteButton = document.getElementById('deleteButton')
    postDeleteButton.onclick = function () {
        deletePost(postID)
    }
}

async function deletePost(postID) {
    const response = await make_request('POST', '/deletepost/', {
        post_id: postID,
    });
    const data = await response.json();
    if (data.success) {
        const userBlock = document.getElementById(postID)
        userBlock.remove()
        recountRows()
    }
    return data
}
