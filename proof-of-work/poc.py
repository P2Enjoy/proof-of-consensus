import hashlib

"""
In this example, I create a PoW class which has a mine method that takes in some
data and mines a nonce (a random number) that satisfies the PoW condition by 
repeatedly hashing the data concatenated with the nonce. 
The difficulty of mining is defined by the difficulty parameter, which determines
how many leading zeroes the hash must have. 

In this example, I change the difficulty progressivlely to 6, so the hash must have up to 6 leading zeroes. 
The method mine uses sha256 as the hashing function, but other algorithms could be used as well.
In the last lines of the script, I created an instance of PoW with difficulty changing from none to 6 and then I call 
the mine method with a string "example data" and it will print the number (nonce) which meets the difficulty along 
with the time required for the operation.

Please note that this is a simple PoW algorithm to demonstrate how it works, and it's not secure for real-world usage, 
as it does not add any extra security measures or protection. 
Also, it does not consider the timeliness and performance for real-world usage you should consider more secure 
alternatives for implementing PoW algorithm in your projects
"""
class PoW:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def mine(self, data):
        target = "0" * self.difficulty
        nonce = 0
        while True:
            # Create the hash of the data and the nonce
            h = hashlib.sha256()
            h.update(f"{data}{nonce}".encode())
            digest = h.hexdigest()
            if digest[:self.difficulty] == target:
                return nonce
            nonce += 1


# Example usage:
import time

data = "example data"
for i in range(7):
    pow = PoW(i)

    st = time.process_time_ns()
    print(pow.mine(data))
    et = time.process_time_ns()

    # get execution time
    res = et - st
    print('CPU Execution time:', res, 'nanoseconds', 'to mine with a difficulty of', i)
