import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import random

n = 10
a = 3
M = 2000
K = 120
sigma = 1
gamma = 0.99

def calculate_z_value():
    z = stats.norm.ppf((1 + gamma) / 2)
    return z

def generate_sample():
    return np.random.normal(a, sigma, n)

def print_basic_stats(data):
    print("Mean =", np.mean(data))
    print("Var =", np.var(data))
    print("Std =", np.std(data))

def confidence_interval_known_sigma(data):
    z = calculate_z_value()
    delta = z * sigma / math.sqrt(len(data))
    mean = np.mean(data)
    return mean - delta, mean + delta

def confidence_interval_unknown_sigma(data):
    t = stats.t.ppf((1 + gamma) / 2, df=len(data))
    s = np.std(data)
    delta = t * s / math.sqrt(len(data))
    mean = np.mean(data)
    return mean - delta, mean + delta

def plot_interval_length_by_n():
    length1 = []
    length2 = []
    ns = []

    for i in range(100, 1000):
        data = np.random.normal(a, sigma, i)
        mean = sum(data) / len(data)

        inter1 = stats.norm.interval(gamma, loc=mean, scale=sigma / math.sqrt(i))
        length1.append(inter1[1] - inter1[0])

        s = np.std(data)
        inter2 = stats.norm.interval(gamma, loc=mean, scale=s / math.sqrt(i))
        length2.append(inter2[1] - inter2[0])

        ns.append(i)

    plt.plot(ns, length1, label="Known sigma")
    plt.plot(ns, length2, label="Unknown sigma")
    plt.legend()
    plt.grid()
    plt.show()

def plot_interval_length_by_gamma():
    gamma_values = np.linspace(0.5, 0.999, 200)
    length = []
    length2 = []

    for g in gamma_values:
        data = generate_sample()
        mean = np.mean(data)

        inter = stats.norm.interval(g, loc=mean, scale=sigma / math.sqrt(n))
        length.append(inter[1] - inter[0])

        s = np.std(data)
        inter = stats.norm.interval(g, loc=mean, scale=s / math.sqrt(n))
        length2.append(inter[1] - inter[0])

    plt.plot(gamma_values, length)
    plt.plot(gamma_values, length2)
    plt.show()

def variance_confidence_interval_length():
    gamma_values = np.linspace(0.5, 0.99, 50)
    lengths = []

    for g in gamma_values:
        chi_l = stats.chi2.ppf((1 - g) / 2, df=n)
        chi_u = stats.chi2.ppf((1 + g) / 2, df=n)

        data = generate_sample()
        sample_var = np.var(data)

        length = (n) * sample_var * (1 / chi_l - 1 / chi_u)
        lengths.append(length)

    plt.plot(gamma_values, lengths)
    plt.show()

def monte_carlo_gamma_estimation():
    cover = 0
    i = 0
    while i < M:
        data = np.random.normal(a, sigma, n)
        mean = np.mean(data)
        std = np.std(data)

        t = stats.t.ppf((1 + gamma) / 2, df=n)
        delta = t * std / math.sqrt(n)

        if mean - delta < a < mean + delta:
            cover = cover + 1

        i = i + 1

    return cover / M

def main():
    data = generate_sample()

    print_basic_stats(data)

    ci1 = confidence_interval_known_sigma(data)
    print("CI known sigma:", ci1)

    ci2 = confidence_interval_unknown_sigma(data)
    print("CI unknown sigma:", ci2)

    plot_interval_length_by_n()
    plot_interval_length_by_gamma()
    variance_confidence_interval_length()

    gamma_star = monte_carlo_gamma_estimation()
    print("Gamma* =", gamma_star)

if __name__ == "__main__":
    main()
