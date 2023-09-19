    import time
    import threading
    import logging
    from .models import UnverifiedUser
    def shut_down(params):
        # Do some stuff
        # Offload the blocking job to a new thread

        t = threading.Thread(target=email_verification_clearer, args=(), kwargs={})
        t.setDaemon(True)
        t.start()

        return True

    def email_verification_clearer():
        while True:
            print("checked codes")
            unverified_users = UnverifiedUser.objects.all()
            for user in unverified_users:
                user.remove_token_if_expired()
            time.sleep(10)
    print("IM HERJES")
    shut_down()