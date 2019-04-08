from proso2_newscript import prosoWeb

P = prosoWeb()
P.start_constrained_exact(600)
P.DbInterface.close_connection()
