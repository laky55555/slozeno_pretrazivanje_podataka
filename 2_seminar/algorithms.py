import math

##euklidska udaljenost
##jednostavnije numpy.linalg.norm()
def udaljenost(a, b):
    sum = 0
    for ai, bi in zip(a, b):
        sum += (ai - bi) ** 2
    return math.sqrt(sum)


def iteracija(X, C, m, w):
    brojnik = X[0]
    for b in brojnik: b = 0
    nazivnik = 0
    noviC = set()
    for cj in C:
        for xi in X:
            nazivnik += m(cj, xi)*w(xi)
            for xij in xi:
                xij *= m(cj, xi)*w(xi)
            i = 0
            for bi in brojnik:
                bi += xi[i]
                ++i
        for b in brojnik:
            b /= float(nazivnik)
        noviC.add(brojnik)
    return noviC


## K-means

class KMeans():

    def KMf(X, C):
        sum = 0
        for x in X:
            min = math.inf
            for c in C:
                if udaljenost(x, c)**2 < min:
                    min = udaljenost(x, c)**2
            sum += min
        return sum


    def KMm(C, cj, xi):
        min = udaljenost(cj, xi)**2
        for c in C:
            if udaljenost(c, xi)**2 < min:
                return 0
        return 1


    def KMw(xi):
        return 1

## GEM

class GaussianExpectationMaximization():
    ## p - Gauss
    def p(c):
        return norm(c, 1).pdf(x)

    def p2(x,c):
        return ##nez


    def GEMf(X, C):
        rez = 0
        for x in X:
            b = 0
            for c in C:
                b += p2(x, c)*p(c)
            rez += math.log(b)
        return -rez


    def GEMm(cj, xi):
        return p2(xi, cj)*p(cj)/p(xi)


    def GEMw(xi):
        return 1


##FKM

class FuzzyKMeans():

    def FKMf(U, X, C):
        rez = 0
        for xi in X:
            b = 0
            for cj in C:
                b += U[i][j] * udaljenost(xi, cj)**2
            rez += b
        return rez


    def FKMm(r, C, cj, xi):
        brojnik = udaljenost(xi, cj)**(-2/(r-1))
        nazivnik = 0
        for c in C:
            nazivnik += udaljenost(xi, c)**(-2/(r-1))
        return brojnik/nazivnik


    def FKMw(xi):
        return 1

##KHM

class KHarmonicMeans:
    def KHMf(p, X, C):
        rez = 0
        for xi in X:
            brojnik = len(C)
            nazivnik = 0
            for cj in C:
                nazivnik += 1/(udaljenost(xi, cj)**p)
        rez += brojnik/nazivnik
        return rez


    def KHMm(p, C, cj, xi):
        brojnik = udaljenost(xi, cj)**(-p-2)
        nazivnik = 0
        for c in C:
            nazivnik += udaljenost(xi, c)**(-p-2)
        return brojnik/nazivnik


    def KHMw(p, C, xi):
        brojnik = 0
        for c in C:
            brojnik += udaljenost(xi, c)**(-p-2)
        nazivnik = 0
        for c in C:
            nazivnik += udaljenost(xi, c)**(-p)
        nazivnik **= 2
        return brojnik/nazivnik
