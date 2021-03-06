
import numpy as np
from random import random, shuffle
from Bio import SeqIO

MILLION = 1000 * 1000


def seq_to_matrix(seq):
    """Return a four color indicator encoding of a sequence as a row 'vector'."""
    seq = seq.upper()
    return np.array([
        [1 if seqb == base else 0 for seqb in seq] for base in 'ACGT'
    ])


class ShortReadData:

    def __init__(self, seq_len, seqs=None):
        self.index = None
        self.seq_len = seq_len
        self.alphabet_len = 4
        if seqs is None:
            self.seqs = []

    def __len__(self):
        return len(self.seqs)

    def __getitem__(self, i):
        return self.seqs[i % len(self)]

    def reset(self):
        self.order = list(range(len(self.seqs)))
        shuffle(self.order)
        self.index = 0

    def process_seq(self, seq):
        diff = len(seq) - self.seq_len
        diff //= 2
        return seq_to_matrix(seq[diff:(diff + self.seq_len)])

    def flatten(self, seq):
        if len(seq.shape) == 3:
            return np.reshape(seq, [seq.shape[0], seq.shape[1] * seq.shape[2]])
        return np.reshape(seq, [seq.shape[1] * seq.shape[2]])

    def unflatten(self, seq):
        if len(seq.shape) == 3:
            return np.reshape(seq, [seq.shape[0], self.alphabet_len, self.seq_len])
        return np.reshape(seq, [self.alphabet_len, self.seq_len])

    def next_batch(self, batch_size, flat=True, type=np.float64):
        if self.index is None:
            self.reset()

        batch = []
        for _ in range(batch_size):
            ind = self.order[self.index]
            seq = self.seqs[ind]
            self.index = (self.index + 1) % len(self.seqs)
            if self.index == 0:
                self.reset()
            batch.append(self.process_seq(seq))
        return np.array(batch)


class FastqSeqData:

    def __init__(self, filename, seq_len=100, split_frac=0.8, total=MILLION):
        self.train, self.test = ShortReadData(seq_len), ShortReadData(seq_len)
        with open(filename) as fastq_handle:
            for i, rec in enumerate(SeqIO.parse(fastq_handle, "fastq")):
                if i >= total:
                    break
                if random() < split_frac:
                    self.train.seqs.append(rec.seq)
                else:
                    self.test.seqs.append(rec.seq)
