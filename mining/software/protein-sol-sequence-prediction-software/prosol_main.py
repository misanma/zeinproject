from recover import prosol
P = prosol()
P.recover()

'''from prosol_script import prosol

P = prosol()
P.start_unconstrained_upto(20, 10)
P.start_unconstrained_fixed(20, 10)
P.start_constrained_upto(20, 10, 2, 2)
P.start_constrained_fixed(20, 10, 2, 2)
P.DbInterface.close_connection()
'''
