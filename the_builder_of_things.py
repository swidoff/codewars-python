class Name(object):
    def __init__(self):
        self.value = None

    def __str__(self):
        return self.value


name = Name()


class Getattr(object):
    def __init__(self, setter):
        self.setter = setter

    def __getattr__(self, item):
        return self.setter(item)


class Things(tuple):

    @property
    def each(self):
        return self

    def having(self, count):
        def update_all(item):
            res = []
            for t in self:
                component = getattr(t.has(count), item)
                if isinstance(component, Things):
                    res.extend(component)
                else:
                    res.append(component)

            return Things(res)

        return Getattr(update_all)

    @property
    def being_the(self):
        def update_all(relationship, value):
            for t in self:
                getattr(getattr(t.is_the, relationship), value)
            return self.each

        return Getattr(lambda relationship: Getattr(lambda value: update_all(relationship, value)))

    @property
    def and_the(self):
        return self.being_the


class Thing(object):
    def __init__(self, name):
        self.name = name
        self._is = set()
        self._has = {}

    @property
    def is_a(self):
        return Getattr(lambda p: self._is.add(p))

    @property
    def is_not_a(self):
        return Getattr(lambda p: self._is.remove(p) if p in self._is else None)

    def has(self, count: int):
        def update(p):
            if count > 1:
                self._has[p] = Things(Thing(p[:-1] if p.endswith("s") else p) for _ in range(count))
            else:
                self._has[p] = Thing(p)
            return self._has[p]

        return Getattr(update)

    def having(self, count: int):
        return self.has(count)

    @property
    def is_the(self):
        def update(relationship, value):
            self._has[relationship] = value

        return Getattr(lambda relationship: Getattr(lambda value: update(relationship, value)))

    @property
    def can(self):
        def update(verb):
            def register(callable, past_tense=None):
                if past_tense:
                    self._has[past_tense] = []

                def call(*args, **kwargs):
                    global name
                    name.value = self.name
                    res = callable(*args, **kwargs)
                    if past_tense:
                        self._has[past_tense].append(res)
                    return res

                self._has[verb] = call

            return register

        return Getattr(update)

    def __getattr__(self, item):
        if item.startswith("is_a_"):
            return item[len("is_a_"):] in self._is
        elif item.startswith("is_"):
            return item[len("is_"):] == self.name
        elif item in self._has:
            return self._has[item]


if __name__ == '__main__':
    from test import Test as test

    jane = Thing('Jane')
    test.describe('jane =  Thing("Jane")')
    test.describe('jane.name')
    test.it('should be "Jane"')
    test.assert_equals(jane.name, 'Jane')

    test.describe('#is_a')
    test.describe('is_a.woman (dynamic key)')
    jane.is_a.woman
    test.it('jane.is_a_woman should return true')
    test.assert_equals(jane.is_a_woman, True)

    test.describe('#is_not_a')
    test.describe('is_not_a.man (dynamic key)')
    jane.is_not_a.man
    test.it('jane.is_a_man should return false')
    test.assert_equals(jane.is_a_man, False)

    test.describe('#has')

    test.describe('jane.has(2).arms')
    jane = Thing('Jane')
    jane.has(2).arms
    test.it('should define an arms method that is tuple subclass')
    test.assert_equals(isinstance(jane.arms, tuple), True)
    test.it('should populate 2 new Thing instances within the tuple subclass')
    test.assert_equals(len(jane.arms), 2)
    test.assert_equals(all(isinstance(v, Thing) for v in jane.arms), True)
    test.it('should call each thing by its singular form (aka "arm")')
    test.assert_equals(all(v.name == "arm" for v in jane.arms), True)
    test.it('should have is_arm == true for each arm instance')
    test.assert_equals(all(v.is_arm for v in jane.arms), True)

    test.describe('jane.having(2).arms (alias)')
    test.it('should populate 2 new Thing instances within the tuple subclass')
    jane = Thing('Jane')
    jane.having(2).arms
    test.assert_equals(len(jane.arms), 2)
    test.assert_equals(all(isinstance(v, Thing) for v in jane.arms), True)

    test.describe('jane.has(1).head')
    jane = Thing('Jane')
    jane.has(1).head
    test.it('should define head method that is a reference to a new Thing')
    test.assert_equals(isinstance(jane.head, Thing), True)
    test.it('should name the head thing "head"')
    test.assert_equals(jane.head.name, "head")

    test.describe('jane.has(1).head.having(2).eyes')
    jane = Thing('Jane')
    jane.has(1).head.having(2).eyes
    test.it('should create 2 new things on the head')
    test.assert_equals(len(jane.head.eyes), 2)
    test.assert_equals(all(isinstance(v, Thing) for v in jane.head.eyes), True)
    test.it('should name the eye things "eye"')
    test.assert_equals(all(v.name == 'eye' for v in jane.head.eyes), True)

    test.describe('#each')
    test.describe('jane.has(2).arms.each.having(5).fingers')
    jane = Thing('Jane')
    jane.has(2).arms.each.having(5).fingers
    test.it('should cause 2 arms to be created each with 5 fingers')
    test.assert_equals(all(len(v.fingers) == 5 for v in jane.arms), True)

    test.describe('#is_the')

    test.describe('jane.is_the.parent_of.joe')
    jane = Thing('Jane')
    jane.is_the.parent_of.joe
    test.it('should set jane.parent_of == "joe"')
    test.assert_equals(jane.parent_of, "joe")

    test.describe('#being_the')

    test.describe('jane.has(1).head.having(2).eyes.each.being_the.color.blue')
    test.it("jane's eyes should both be blue")
    jane = Thing('Jane')
    jane.has(1).head.having(2).eyes.each.being_the.color.blue
    test.assert_equals(all(v.color == 'blue' for v in jane.head.eyes), True)

    test.describe('jane.has(2).eyes.each.being_the.color.blue.and_the.shape.round')
    test.it('should allow chaining via the and_the method')
    jane = Thing('Jane')
    jane.has(2).eyes.each.being_the.color.blue.and_the.shape.round
    test.assert_equals(all(v.color == 'blue' for v in jane.eyes), True)
    test.assert_equals(all(v.shape == 'round' for v in jane.eyes), True)

    test.describe('jane.has(2).eyes.each.being_the.color.green.having(1).pupils.each.being_the.color.black')
    test.it('should allow nesting by using having')
    jane = Thing('Jane')
    jane.has(2).eyes.each.being_the.color.green.having(1).pupil.being_the.color.black
    test.assert_equals(all(v.color == 'green' for v in jane.eyes), True)
    test.assert_equals(all(v.pupil.color == 'black' for v in jane.eyes), True)

    test.describe('#can')

    test.describe('jane.can.speak(lambda phrase: "#%s says: #%s" % (name, phrase))')
    jane = Thing('Jane')


    def fnc(phrase):
        return "%s says: %s" % (name, phrase)


    jane.can.speak(fnc)
    test.it('should create a speak method on the instance')
    test.assert_equals(jane.speak('hi'), "Jane says: hi")

    test.describe('jane.can.speak(lambda phrase: "#%s says: #%s" % (name, phrase), "spoke")')
    jane = Thing('Jane')
    fnc = lambda phrase: "%s says: %s" % (name, phrase)
    jane.can.speak(fnc, 'spoke')
    jane.speak('hi')
    test.it('should add a "spoke" attribute that tracks all speak call results')
    test.assert_equals(jane.spoke, ["Jane says: hi"])
    jane.speak('goodbye')
    test.assert_equals(jane.spoke, ["Jane says: hi", "Jane says: goodbye"])
