from proso2_newscript import prosoWeb

P = prosoWeb()
P.start_unconstrained_exact(550)
P.DbInterface.close_connection()
