import os
import random
import re
import time
import os.path
import psycopg2
from subprocess import call
from squence_maker import SequenceMaker
from database_interface import DbInterface


class prosol:
    """interface of proso predictor"""
    #	initialize evironment

    def __init__(self):
        print("Initializing PROSOII script...")
        self.n = 0

        #	set up the SequenceMaker
        OrigSeq = '''MATKILALLALLALLVSATNAFIIPQCSLAPSASIPQFLPPVTSMGFEHPAVQAYRLQLALAASALQQPIAQLQQQSLAHLTLQTIATQQQQQQFLPSLSHLAVVNPVTYLQQQLLASNPLALANVAAYQQQQQLQQFMPVLSQLAMVNPAVYLQLLSSSPLAVGNAPTYLQQQLLQQIVPALTQLAVANPAAYLQQLLPFNQLAVSNSAAYLQQRQQLLNPLAVANPLVATFLQQQQQLLPYNQFSLMNPALQQPIVGGAIF'''
        self.SequenceMaker = SequenceMaker(OrigSeq)

        #	initialize database interface
        self.DbInterface = DbInterface('zeinsolub',
                                       'prosol')

        conn = psycopg2.connect("dbname=zeinsolub")
        cur = conn.cursor()
        cur.execute("SELECT seq FROM proso2")
        self.material = cur.fetchall()

        cur.close()
        conn.close()

        self.index = 0
        self.leng = len(self.material)

        print("Initialized")
        return

    #	Begin scrapping 5 sequences input for n times
    #	Unconstrained version
    def recover(self):
        print("Begin Recover...")
        while self.index < self.leng:
            row = []
            buffer = []
            sequenceBuffer = []
            # for i in range(n):
            with open("sequence.fasta", "w") as se:
                for i in range(50):
                    randomSequence = self.material[self.index][0]
                    sequenceBuffer.append(randomSequence)
                    se.write(">sample" + str(i) + "\n")
                    se.write(randomSequence + "\n")
                    self.index += 1
                print("------50 rows done------")
            call(["./multiple_prediction_wrapper_export.sh", "sequence.fasta"])

            while not os.path.exists("seq_prediction.txt"):
                time.sleep(.1)

            coun = 0
            with open("seq_prediction.txt", "r") as rs:
                for line in rs:
                    if line.startswith("SEQUENCE PREDICTIONS"):
                        nline = line.split(",")
                        solub = float(nline[3])
                        deter = True if solub > 0.45 else False
                        #print(solub, deter)
                        ranseq = sequenceBuffer[coun]
                        aa_count_list, charge = self.SequenceMaker.count_aa_difference(
                            ranseq)
                        row = [deter, solub, sum(
                            aa_count_list), charge] + aa_count_list + [ranseq]
                        buffer.append(row)
                        coun += 1
            call(["rm", "seq_prediction.txt"])
            # print(coun)
            for eachrow in buffer:
                self.DbInterface.insert(eachrow)
                self.n += 1
                #print('---Written ' + str(self.n) + ' rows---')
        return 0
