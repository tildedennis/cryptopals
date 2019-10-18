import random
import time

import challenge21


def get_rng_output():
    rand_secs = random.randrange(40, 1000)
    time.sleep(rand_secs)

    mt19937 = challenge21.MT19937()
    timestamp = int(time.time())
    mt19937.seed_mt(timestamp)

    rand_secs = random.randrange(40, 1000)
    time.sleep(rand_secs)

    output = mt19937.extract_number()

    return output, timestamp


def discover_seed(output):
    test_seed = int(time.time())

    while test_seed:
        mt19937 = challenge21.MT19937()
        mt19937.seed_mt(test_seed)
        if mt19937.extract_number() == output:
            return test_seed

        test_seed -= 1


if __name__ == "__main__":
    rng_output, check_seed = get_rng_output()

    seed = discover_seed(rng_output)
    if seed and seed == check_seed:
        print "found seed: %d" % seed
