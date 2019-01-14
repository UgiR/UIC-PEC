
def login_request(user, password, webapp):
    user.update(active=True)
    webapp.post_json('/login', dict(
                email=user.email,
                password=password
            ))