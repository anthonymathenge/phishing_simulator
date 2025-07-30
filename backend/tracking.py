from app.database import update_interaction

def record_open(user_id: str):
    update_interaction(user_id, "opened")

def record_click(user_id: str):
    update_interaction(user_id, "clicked")

def record_submission(user_id: str):
    update_interaction(user_id, "submitted")
