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
        for x in range(n):
            row = []
            buffer = []
            sequenceBuffer = []
            # for i in range(n):
            with open("sequence.fasta", "w") as se:
                for i in range(50):
                    leng = random.randint(1,
                                          length)
                    randomSequence = self.SequenceMaker.generator_unconstrained(
                        leng)
                    sequenceBuffer.append(randomSequence)
                    se.write(">sample" + str(i) + "\n")
                    se.write(randomSequence + "\n")

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

    def start_unconstrained_fixed(self,
                                  n, length):
        print("Begin Mining uf...")
        for x in range(n):
            row = []
            buffer = []
            sequenceBuffer = []
            # for i in range(n):
            with open("sequence.fasta", "w") as se:
                for i in range(50):
                    randomSequence = self.SequenceMaker.generator_unconstrained(
                        length)
                    sequenceBuffer.append(randomSequence)
                    se.write(">sample" + str(i) + "\n")
                    se.write(randomSequence + "\n")

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

    def start_constrained_upto(self,
                               n, length, negative, positive):
        print("Begin Mining...")
        for x in range(n):
            row = []
            buffer = []
            sequenceBuffer = []
            # for i in range(n):
            with open("sequence.fasta", "w") as se:
                for i in range(50):
                    leng = random.randint(1,
                                          length)
                    randomSequence = self.SequenceMaker.generator_constrained(
                        leng, -negative, positive)
                    sequenceBuffer.append(randomSequence)
                    se.write(">sample" + str(i) + "\n")
                    se.write(randomSequence + "\n")

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

    def start_constrained_fixed(self,
                                n, length, negative, positive):
        print("Begin Mining...")
        for x in range(n):
            row = []
            buffer = []
            sequenceBuffer = []
            # for i in range(n):
            with open("sequence.fasta", "w") as se:
                for i in range(50):
                    leng = length
                    randomSequence = self.SequenceMaker.generator_constrained(
                        leng, -negative, positive)
                    sequenceBuffer.append(randomSequence)
                    se.write(">sample" + str(i) + "\n")
                    se.write(randomSequence + "\n")

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
