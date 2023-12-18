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
    console.log(data);
    return data;
}

async function deleteTaskBlock(taskId) {
    const response = await make_request('POST', '/deletetask/', {
            task_id: taskId,
    });
    const data = await response.json();
    if (data.success){
        const taskBlock = document.getElementById(taskId);
        const tasksBox = taskBlock.parentElement;
        if (tasksBox.childElementCount == 1){
            tasksBox.parentElement.children[0].remove();
        }
        taskBlock.remove();
    }
    console.log(data);
    return data;
}

async function editTaskBlock(taskId){
    // TODO
}