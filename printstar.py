#-*-coding=UTF-8-*-
def printstars(N= 5):
    for i in xrange(N):
        print ' '*(N-1-i), '*'*(2*i+1)
printstars()