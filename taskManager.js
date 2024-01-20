const taskInput = document.getElementById("task");
const priorityInput = document.getElementById("priority");
const deadlineInput = document.getElementById("deadline");
const addTaskButton = document.getElementById("add-task");
const taskList = document.getElementById("task-list");

addTaskButton.addEventListener("click", () => {
    const task = taskInput.value;
    const priority = priorityInput.value;
    const deadline = deadlineInput.value;
    
    if (task.trim() === "" || deadline === "") {
        alert("Please enter a task and select an upcoming date for the deadline.");
        return; 
    }

    const selectedDate = new Date(deadline);
    const currentDate = new Date();

    if (selectedDate <= currentDate) {
        alert("Please select an upcoming date for the deadline.");
        return; 
    }

    const taskData = {
        task: task,
        priority: priority,
        deadline: deadline
    };

    // Send the task data to the server using fetch
    fetch('/add_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If the task was successfully added, update the UI
            const taskItem = document.createElement("div");
            taskItem.classList.add("task");
            taskItem.innerHTML = `
                <p>${task}</p>
                <p>Priority: ${priority}</p>
                <p>Deadline: ${deadline}</p>
                <button class="mark-done">Mark Done</button>
            `;

            taskList.appendChild(taskItem);

            taskInput.value = "";
            priorityInput.value = "top";
            deadlineInput.value = "";
        } else {
            alert("Error adding task. Please try again.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error adding task. Please try again.");
    });
});

taskList.addEventListener("click", (event) => {
    if (event.target.classList.contains("mark-done")) {
        const taskItem = event.target.parentElement;
        taskItem.style.backgroundColor = "#f2f2f2";
        event.target.disabled = true;
    }
});