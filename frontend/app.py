from nicegui import ui
import requests

API_URL = 'http://backend:5000/api'

def fetch_todos():
    """Get all todos from API"""
    try:
        response = requests.get(f'{API_URL}/todos')
        return response.json()
    except:
        return []

def create_todo(title):
    """Create new todo via API"""
    requests.post(f'{API_URL}/todos', json={'title': title})

def toggle_todo(todo_id, completed):
    """Toggle todo completion via API"""
    requests.put(f'{API_URL}/todos/{todo_id}', json={'completed': not completed})

def delete_todo(todo_id):
    """Delete todo via API"""
    requests.delete(f'{API_URL}/todos/{todo_id}')

@ui.page('/')
def main_page():
    """Simple todo list UI"""
    
    def refresh():
        """Refresh the todo list"""
        todo_container.clear()
        with todo_container:
            todos = fetch_todos()
            if not todos:
                ui.label('No todos yet. Add one below!')
            else:
                for todo in todos:
                    with ui.row().classes('items-center gap-2'):
                        checkbox = ui.checkbox(
                            value=todo['completed'],
                            on_change=lambda e, tid=todo['id'], comp=todo['completed']: 
                                (toggle_todo(tid, comp), refresh())
                        )
                        ui.label(todo['title']).classes(
                            'line-through' if todo['completed'] else ''
                        )
                        ui.button('Delete', 
                            on_click=lambda tid=todo['id']: (delete_todo(tid), refresh())
                        ).props('flat color=red size=sm')
    
    def add_todo():
        """Add new todo"""
        if title_input.value.strip():
            create_todo(title_input.value.strip())
            title_input.value = ''
            refresh()
    
    ui.label('Todo App').classes('text-3xl font-bold mb-4')
    
    # Input section
    with ui.row().classes('gap-2 mb-4'):
        title_input = ui.input(placeholder='Enter new todo...').classes('flex-grow')
        ui.button('Add', on_click=add_todo).props('color=primary')
    
    # Todo list container
    todo_container = ui.column().classes('gap-2')
    
    # Initial load
    refresh()

ui.run(host='0.0.0.0', port=8080, reload=False)

