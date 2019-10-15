class MT19937:

    def __init__(self):
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908B0DF
        self.u = 11
        self.d = 0xFFFFFFFF
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.f = 0x6c078965

        self.MT = [0]*self.n
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (~self.lower_mask) & (2**self.w-1)

    def seed_mt(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i) & (2**self.w-1)

    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
                print "Generator was never seeded"
                return
            self.twist()

        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)

        self.index += 1

        return y & (2**self.w-1)

    def twist(self):
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper_mask) \
                + (self.MT[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ self.a

            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA

        self.index = 0


if __name__ == "__main__":
    mt19937 = MT19937()
    mt19937.seed_mt(5489)

    for i in range(10):
        print mt19937.extract_number()
