import random


def get_ticket():
    ticket = ''
    s = 'abcdefghijkrmnopqrstuvwxyz1234567890'
    for i in range(28):
        r_num = random.choice(s)
        ticket += r_num
    return ticket
