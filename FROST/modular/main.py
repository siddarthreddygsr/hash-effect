from functools import reduce
import numpy as np
import random
import sys
import hashlib
import operator
from fractions import Fraction

class frost:
    def __init__(self, no_of_nodes, threshold, g, p):
        self.no_of_nodes = no_of_nodes
        self.threshold = threshold
        self.g = g
        self.p = p
        self.degree = threshold - 1
        self.q = 23
        self.polynomial_list = []
        self.commit_list = []
        self.k = random.randint(1, 10)
        self.r = g**self.k
        self.message = ""
        self.secrets = []
        self.y = []
        self.u = []
        self.c = []
        self.b = []
        self.signatures = []
        self.d_e_cap = []
        self.d_e = []

    def hash(self, a, b):
        combined_string = str(a) + str(b)
        combined_bytes = combined_string.encode('utf-8')
        sha256_hash = hashlib.sha256(combined_bytes).hexdigest()
        return int(sha256_hash, 16) % self.p

    def create_polynomial(self):
        coefficients = []
        for i in range(self.degree + 1):
            coefficients.append(random.randint(1, 10))
        polynomial = np.poly1d(coefficients)
        return polynomial

    def setup(self):
        for i in range(self.no_of_nodes):
            self.polynomial_list.append(self.create_polynomial())

        for i in self.polynomial_list:
            commit_i = []
            for j in i:
                commit_i.append(pow(self.g, j))
            self.commit_list.append(commit_i)

        for i in range(self.no_of_nodes):
            secret = int(self.polynomial_list[i][0])
            self.secrets.append(secret)
            self.y.append(int(pow(self.g, secret)))

    def generate_signatures(self):
        for i in range(self.no_of_nodes):
            self.c.append(self.hash(self.r, pow(self.g, sum(self.secrets))))

            u_i = self.k + self.hash(self.r, self.y[i]) * self.secrets[i]
            self.u.append(u_i)
            self.signatures.append([u_i, self.r])

    def verify_signatures(self):
        for i in range(self.no_of_nodes):
            lhs = pow(self.g, self.u[i]) % self.p
            rhs = pow(self.y[i], self.c[i]) * self.r % self.p
            print(lhs, rhs)
            if lhs == rhs:
                print(f"Signature {i} is valid")

    def compute_slave_shares(self):
        slave_shares = []
        total_share = []
        for i in range(self.no_of_nodes):
            slave_share = []
            s = 0
            for j in range(self.no_of_nodes):
                share = []
                share.append(i + 1)
                share.append(self.polynomial_list[j](i + 1) % self.p)
                s += self.polynomial_list[j](i + 1) % self.p
                slave_share.append(share)
            slave_shares.append(slave_share)
            total_share.append(s % self.p)
        print(slave_shares)
        print(total_share)

    def compute_global_secret(self):
        global_secret = 1
        for i in self.secrets:
            global_secret *= self.g ** i
        print(global_secret)

    def compute_d_e_cap(self, pi):
        d_e = []
        d_e_cap = []
        for i in range(self.no_of_nodes):
            d_e_i = []
            d_e_cap_i = []
            for i in range(pi):
                d_e_i_pi = []
                d_e_cap_i_pi = []
                d = random.randint(1, 25)
                e = random.randint(1, 25)
                d_cap = pow(self.g, d)
                e_cap = pow(self.g, e)
                d_e_cap_i_pi.append(d_cap)
                d_e_cap_i_pi.append(e_cap)
                d_e_i_pi.append(d)
                d_e_i_pi.append(e)
                d_e_cap_i.append(d_e_cap_i_pi)
                d_e_i.append(d_e_i_pi)
            d_e_cap.append(d_e_cap_i)
            d_e.append(d_e_i)
        print(d_e)
        print(d_e_cap)
        return d_e_cap

    def compute_b(self,pi):
        self.d_e_cap = self.compute_d_e_cap(pi) 
        b = []
        for i in range(self.threshold):
            print(self.d_e_cap)
            temp = [i + 1] + self.d_e_cap[i][0]
            b.append(temp)
        print("b: ", b)

    def compute_p_hash(self, message):
        p_hash = []
        combined_string = message + str(self.verifier)
        for i in range(self.no_of_nodes - 1):
            stringtohash = str(i) + combined_string
            stringtohash = stringtohash.encode('utf-8')
            sha256_hash = hashlib.sha256(stringtohash).hexdigest()
            hashed = int(sha256_hash, 16) % self.p
            p_hash.append(hashed)
        print(p_hash)

    def compute_c_hash(self):
        c_hash = []
        for i in range(self.threshold):
            combined_string = str(self.r) + str(self.y[i]) + self.message
            stringtohash = str(i) + combined_string
            stringtohash = stringtohash.encode('utf-8')
            sha256_hash = hashlib.sha256(stringtohash).hexdigest()
            hashed = int(sha256_hash, 16) % self.p
            c_hash.append(hashed)
        print("c hash : ", c_hash)

    def compute_z(self):
        z = []
        lamdas = []
        for i in range(self.threshold):
            lamda = Fraction(1, 1)
            for j in range(1, i + 1):
                if i != j:
                    lamda *= Fraction(j, j - i)
            lamdas.append(lamda)
            z_i = self.d_e[i][0][0] + self.d_e[i][0][1] * self.p_hash[i] + self.c_hash[i] * self.secrets[i] * lamda
            z.append(z_i)
        z_cap = sum(z)
        print("lamdas : ", lamdas)

        new_r = 1
        for i in range(self.threshold):
            d = self.d_e_cap[i][0][0]
            e = self.d_e_cap[i][0][1]
            r_i = d * pow(e, self.p_hash[i])
            new_r *= r_i
            lhs = pow(self.g, int(z[i]), int(self.p))
            rhs = pow(self.y[i], int(lamdas[i] * self.c_hash[i]), self.p) * r_i % self.p
            print(lhs, rhs)

        lhs = pow(self.g, int(z_cap), self.p)
        comity = pow(self.g, sum(self.secrets), self.p)
        new_c = reduce(operator.mul, self.c_hash)
        # new_c = sum(self.c_hash)
        rhs = pow(comity, new_c, self.p) * new_r % self.p

        print(self.c_hash)
        # lhs = pow(g, int(z_cap), p)
        # comity = pow(g, sum(self.secrets), p)
        # new_c = reduce(operator.mul, self.c_hash)
        # rhs = pow(comity, new_c, p) * new_r % p
        print(lhs, rhs)
        # print(comity)

    def main(self):
        self.setup()
        self.generate_signatures()
        self.verify_signatures()
        self.compute_slave_shares()
        self.compute_global_secret()
        pi = int(input("enter a value for pi : "))
        self.compute_d_e_cap(pi)
        self.compute_b(pi)
        message = input("enter a message : ")
        self.verifier = [message, self.b]
        print("verifier : ", self.verifier)
        self.compute_p_hash(message)
        self.compute_c_hash()
        self.compute_z()

# Usage
if __name__ == "__main__":
    no_of_nodes = int(input("enter no of nodes : "))
    threshold = int(input("enter a value for threshold : "))
    g = int(input("enter a value for g : "))
    p = 11

    # schnorr = frost(no_of_nodes, threshold, g, p)
    # schnorr.main()
