from proso2_newscript import prosoWeb

P = prosoWeb()
P.start_constrained_upto()
P.DbInterface.close_connection()
