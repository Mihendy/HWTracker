async function checkTask(element, task_id, status, user_id){
    try{

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const response = await fetch('/checktask/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                task_id: task_id,
                status: status,
                user_id: user_id,
            })
        })
        if (response.ok) {
            const data = await response.json();
            if (data.success){
                element.classList.toggle('selected-card');
                if (status == 'completed'){
                    element.setAttribute('onclick', "checkTask(this, " + task_id + ", 'incompleted', " + user_id + ");");
                }
                else{
                    element.setAttribute('onclick', "checkTask(this, " + task_id + ", 'completed', " + user_id + ");");
                }
            }
            console.log(data);
            return data;
        } else {
            throw new Error('Error occurred during the fetch request.');
        }
    } catch (error){
        console.error('ERROR: ', error);
        throw error;
    }
}