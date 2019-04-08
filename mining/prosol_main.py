from prosol_script import prosol

P = prosol()
P.start_unconstrained_upto(20, 10)
P.DbInterface.close_connection()
