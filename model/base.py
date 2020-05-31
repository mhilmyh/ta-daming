class Base:
    """
    Kelas Basis yang dijadikan
    acuan untuk metode yang harus
    dimiliki kelas turunannya.
    """

    def initial(self):
        raise NotImplementedError

    def deriv(self):
        raise NotImplementedError

    def integrate(self):
        raise NotImplementedError

    def plot(self):
        raise NotImplementedError
