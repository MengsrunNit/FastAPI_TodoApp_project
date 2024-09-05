const checkboxes = document.querySelectorAll('.todo-checkbox');


checkboxes.forEach(checkbox => {
checkbox.addEventListener('change', function () {
    const row = this.closest('tr');
    const titleCell = row.querySelector('.todo-title');
    const deleteButton = row.querySelector('.delete-btn');

    if (this.checked) {
    titleCell.style.textDecoration = 'line-through';
    deleteButton.style.display = 'inline-block'; // Show the delete button
    } else {
    titleCell.style.textDecoration = 'none';
    deleteButton.style.display = 'none'; // Hide the delete button
    }
});
});
 // Handle delete button click events
 document.addEventListener('click', async function (event) {
    if (event.target && event.target.id.startsWith('deleteBtn-')) {
        const todoId = event.target.id.split('-')[1]; // Extract ID from button's ID

        try {
            const token = getCookie('access_token');
            if (!token) {
                throw new Error('Authentication token not found');
            }

            const response = await fetch(`/todo/todo/${todoId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                // Remove the row from the table
                const row = event.target.closest('tr');
                row.remove();
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    }
});
