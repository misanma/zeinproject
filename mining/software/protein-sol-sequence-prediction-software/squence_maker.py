import random

class SequenceMaker:
    def __init__(self, seq):
        #   loading the input sequence
        self.seq = seq

        #   create a dictionary for charge reference
        self.charged_aa_lookup = {
                'D': -1, 'E': -1,
                'K': 1, 'R': 1, 'H': 1
                }

        #   create a dictionary for all position by their charge
        self.all_positions = self.get_aa_dictionary()

        self.seqenceCharge = self.get_seq_charge(self.seq)

    def get_seq_charge(self, seq):
        charge = 0
        for char in seq:
            if char == 'K':
                charge += 1
            elif char == 'R':
                charge += 1
            elif char == 'H':
                charge += 1
            elif char == 'D':
                charge -= 1
            elif char == 'E':
                charge -= 1
        return charge


    def get_aa_dictionary(self):
        #   use: initialize a hash map of all positions by their charge
        positions = dict()
        for i, aa in enumerate(self.seq):
            positions[i] = self.charged_aa_lookup[aa] \
                if aa in self.charged_aa_lookup \
                else 0
        return positions

    def prepare_positions(self,
                          mode):
        #   use: initialize all positions
        #   switching modes
        positions = []
        det = 1 if mode == "Positive" \
            else -1 if mode == 'Negative' \
            else 0
        #   find the positions
        for key, value in self.all_positions.items():
            if value == det:
                positions.append(key)
        return positions

    def generate_single_ramdom_charged_aa(self, choice):
        #   use: return a random aa string by their charge
        if choice == 1:
            return random.sample("KRH", 1)[0]
        else:
            return random.sample("DE", 1)[0]

    def generator_unconstrained(self,
                              length,
                              ):
        #   use: generate a random sequence with constrained charge difference
        result = self.seq
        #   generate a set of random positions
        positions = random.sample(range(len(self.seq))
                                  , length)
        p_n_difference = random.randint(1, length)
        choice = random.randint(0, 1)
        if choice == 0:
            nam_positive = int((p_n_difference + length)/2)
            num_negative = length - nam_positive
        else:
            num_negative = int((p_n_difference + length)/2)
            nam_positive = length - num_negative

        aa_set = [self.generate_single_ramdom_charged_aa(0) for i in range(num_negative)]\
                 + [self.generate_single_ramdom_charged_aa(1) for j in range(nam_positive)]

        #   Finally edit original sequence and return
        for index, pos in enumerate(positions):
            result = result[0:pos] \
                 + aa_set[index] \
                 + result[pos+1:]
        return result

    def generator_constrained(self,
                              length,
                              lower_constrain, upper_constrain,
                              ):
        #   use: generate a random sequence with constrained charge difference
        result = self.seq
        #   generate a set of random positions
        positions = random.sample(range(len(self.seq))
                                  , length)

        #   calculate net charge ---> constrain of the difference between #
        net_charge = 0
        for pos in positions:
            if self.all_positions[pos] == 1:
                net_charge += 1
            elif self.all_positions[pos] == -1:
                net_charge -= 1
        #   Generate the difference in number between positively charged aa and negatively charged ones
        p_n_difference = random.randint(lower_constrain
                                        + net_charge,
                                        upper_constrain
                                        + net_charge)

        nam_positive = int((p_n_difference + length)/2)
        num_negative = length - nam_positive

        #   Create a random set of aa string based on the result above
        aa_set = [self.generate_single_ramdom_charged_aa(0) for i in range(num_negative)]\
                 + [self.generate_single_ramdom_charged_aa(1) for j in range(nam_positive)]
        #   Finally edit original sequence and return
        for index, pos in enumerate(positions):
            result = result[0:pos] \
                 + aa_set[index] \
                 + result[pos+1:]
        return result

    def count_aa_difference(self, RandSeq):
        if len(RandSeq) != len(self.seq):
            print(len(RandSeq), len(self.seq))
            print("Sequence length does not match")
            raise ValueError
        else:
            result = [0 for x in range(5)]
            for index in range(len(self.seq)):
                aa = RandSeq[index]
                if RandSeq[index] != self.seq[index]:
                    if aa == 'K':
                        result[0] += 1
                    elif aa == 'R':
                        result[1] += 1
                    elif aa == 'H':
                        result[2] += 1
                    elif aa == 'D':
                        result[3] += 1
                    elif aa == 'E':
                        result[4] += 1
            charge = self.get_seq_charge(RandSeq)
            return result, charge
