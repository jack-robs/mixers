class Router: 

    def __init__(self, entity1_name, port1, entity2_name, port2):
        self.e1 = entity1_name
        self.e1_port = port1
        self.e2 = entity2_name
        self.e2_port = port2
        #user_str:pubk_int
        self.registered_users = {self.e1:port1, self.e2:port2}
    
    def reg_user(self, user, pubk):
        print("setting " + user + " pubk to " + str(pubk))
        self.registered_users['user'] = pubk



    