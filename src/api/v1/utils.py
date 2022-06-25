from db.models import UserSession


def user_session_to_dict(user_session: UserSession) -> dict:
    as_dict = user_session.__dict__
    as_dict.pop('_sa_instance_state')
    as_dict.pop('id')
    as_dict['user_id'] = str(as_dict['user_id'])
    as_dict['created_at'] = str(as_dict['created_at'])
    return as_dict
