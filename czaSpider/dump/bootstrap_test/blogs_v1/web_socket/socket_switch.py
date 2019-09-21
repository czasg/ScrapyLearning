from web_socket.socket_state import state_code


class Switch:
    valid_case = {str(state): 'case' + str(state) for state in state_code}

    @classmethod
    def case(cls, request, state, message, to):
        return getattr(cls, state)(request, message, to)

    @classmethod
    def w11(cls, request, message, to):
        if request.send_msg_p2g(message, 'connectors', to):
            pass
        else:
            return False
