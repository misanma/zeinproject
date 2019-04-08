import os
import random
import re
import time
import os.path
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
        print("Initialized")
        return

    #	Begin scrapping 5 sequences input for n times
    #	Unconstrained version
    def start_unconstrained_upto(self,
                                 n, length):
        print("Begin Mining...")
        row = []
        for i in range(n):
            leng = random.randint(1,
                                  length)
            randomSequence = self.SequenceMaker.generator_unconstrained(
                leng)
            with open("./software/prosol/sequence.fasta", "w") as se:
                se.write(">sample" + "\n")
                se.write(randomSequence)
                call(
                    ["./software/prosol/multiple_prediction_wrapper_export.sh", "sequence.fasta"])
                while not os.path.exists("seq_prediction.txt"):
                    time.sleep(.1)
                with open("./software/prosol/seq_prediction.txt", "r") as rs:
                    for line in rs:
                        if line.startswith("SEQUENCE PREDICTIONS"):
                            nline = line.split(",")
                            solub = nline[3]
                            deter = True if solub > 0.45 else False
                        else:
                            raise ValueError

                call(["rm", "seq_prediction.txt"])
                aa_count_list, charge = self.SequenceMaker.count_aa_difference(
                    randomSequence)
                row = [deter, solub, sum(
                    aa_count_list), charge] + aa_count_list + [randomSequence]

                self.DbInterface.insert(row)
                self.n += 1
                print('---Written ' + str(self.n) + ' rows---')
        return 0
