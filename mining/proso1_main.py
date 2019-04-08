from proso1_webscript import prosoWeb

P = prosoWeb()
#P.start_constrained_fixed(200, 10, 2, 2)
#P.start_constrained_upto(200, 10, 2, 2)
#P.start_unconstrained_fixed(200, 10)
#P.start_unconstrained_upto(200, 50)
#P.generate_file_unconstrained_upto(1000, 50)
P.generate_file_unconstrained_exact(1000, 50)
P.generate_file_constrained_upto(1000, 50)
P.generate_file_constrained_exact(1000, 50)
P.DbInterface.close_connection()
