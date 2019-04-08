from ccsol_webscript import ccsolWeb

P = ccsolWeb("http://service.tartaglialab.com/email_redir/183270/de23c2ac2b")
P.start("c_exact50_sequence.fasta")
P.DbInterface.close_connection()
