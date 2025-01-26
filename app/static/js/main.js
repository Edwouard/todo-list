document.addEventListener('DOMContentLoaded', function() {
    // Gestion des formulaires
    const todoForm = document.getElementById('todo-form');
    if (todoForm) {
        todoForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/action', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    window.location.reload();
                }
            } catch (error) {
                console.error('Erreur:', error);
            }
        });
    }
    
    // Toggle status des tâches
    document.querySelectorAll('.toggle-status').forEach(btn => {
        btn.addEventListener('click', async function() {
            const taskId = this.dataset.taskId;
            try {
                const response = await fetch(`/done?_id=${taskId}`);
                if (response.ok) {
                    window.location.reload();
                }
            } catch (error) {
                console.error('Erreur:', error);
            }
        });
    });
});