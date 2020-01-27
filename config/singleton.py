def singleton(myClass):
    instances={}
    def get_instance(*args,**kwargs):

        if myClass not in instances:

            instances[myClass]=myClass(*args,**kwargs)
            print(instances)
        return instances[myClass]
    return get_instance

