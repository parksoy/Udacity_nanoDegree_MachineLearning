class Person(object):
    def __init__(self,name):
        self.name=name

    def reveal_identity(self):
        print "My name is {}".format(self.name)


class Superhero(Person):
    def __init__(self,name,hero_name):
        super(Superhero,self).__init__(name)
        self.hero_name=hero_name

    def reveal_identity(self):
        super(Superhero,self).reveal_identity()
        print "And I am {}".format(self.hero_name)

soyoung=Person('Soyoung')
soyoung.reveal_identity()

brian=Superhero('Brian','GeniousBoy')
brian.reveal_identity()
